from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
from os import listdir, remove
from django.conf import settings
from time import sleep
from brazil.models import StateData
from city.models import CityData
from world.models import CountryData
import datetime
import sys


def instantiate_webdriver():
    """
    Create a webdriver instance
    """
    print("Opening webdriver instance...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver", options=chrome_options
    )
    return driver


def access_url_of_ms(driver):
    """
    Access the url of Ministerio da Saude
    """
    print("Accessing url...")
    url = "https://covid.saude.gov.br/"
    driver.get(url)
    return driver


def find_the_clickable_button_of_xlsx_file_and_download_file(driver):
    """
    Find the specific button to download the xlsx file, download it and
    return this file.
    """
    print("Searching for clickable button...")
    try:
        list_of_buttons = driver.find_elements_by_tag_name("ion-button")
        if list_of_buttons:
            for button in list_of_buttons:
                if button.text == "Arquivo CSV":
                    print("Button found! Downloading xlsx file...")
                    button.click()
        else:
            print("There is no ion-button to click")
        files = listdir(".")
        xlsx_file = [file for file in files if file.endswith("xlsx")]

        while not xlsx_file:
            files = listdir(".")
            xlsx_file = [file for file in files if file.endswith("xlsx")]
    except TimeoutException:
        print(
            "Timeout Exception! The file cannot be downloaded. Try again later."
        )
        sys.exit()
    driver.quit()

    return xlsx_file[0]


def pipeline_to_download_xlsx_file():
    """
    Create the driver instance, find the button of file and download it.
    """
    print("Starting the pipeline to download xlsx file...")
    driver = instantiate_webdriver()
    driver = access_url_of_ms(driver)
    xlsx_file = find_the_clickable_button_of_xlsx_file_and_download_file(
        driver
    )
    return xlsx_file


def open_xlsx_file_with_pandas(xlsx_file):
    """
    Open the xlsx file and return the pandas dataframe.
    """
    print("Opening dataframe...")
    df = pd.read_excel(xlsx_file)

    return df


def filter_dataframe_to_find_data_of_specific_date(df, date):
    """
    Get the data of a specific date.
    """
    print("Filtering dataframe...")
    df_filtered_by_date = df[df["data"] == date]
    return df_filtered_by_date


def cleanup_dataframe(df):
    """
    The codmun column is a float column, this must be a int or a string without
    floating point
    """
    print("Cleaning up dataframe data...")
    df[["codmun"]] = df[["codmun"]].fillna(0).astype(int).astype(str)
    df[["municipio"]] = df[["municipio"]].fillna(False)
    return df


def save_brazil_instance_using_ms_source(row):
    """
    Save a CountryData instance with Brazil data
    from Ministerio da Saude source
    """
    print("Saving Brazil data if it does not exist yet...")
    CountryData.objects.create(
        country="Brazil",
        translated_country_name="Brasil",
        date=row.data,
        confirmed=row.casosAcumulado,
        deaths=row.obitosAcumulado,
        active=row.emAcompanhamentoNovos,
        recovered=row.Recuperadosnovos,
        latitude=0,
        longitude=0,
    )


def save_state_instance_using_ms_source(row):
    """
    Save a state instance to database using Ministerio da Saude
    data
    """
    print("Save state data if it does not exist yet...")
    estimated_population_2019 = (
        StateData.objects.filter(state=row.estado)
        .order_by("date")
        .last()
        .estimated_population_2019
    )
    if estimated_population_2019:
        StateData.objects.create(
            state=row.estado,
            estimated_population_2019=estimated_population_2019,
            confirmed=row.casosAcumulado,
            date=row.data,
            deaths=row.obitosAcumulado,
            update_source="MS",
        )
    else:
        print("Não achei")


def save_city_instance_using_ms_source(row):
    """
    Save a city instance to database using Ministerio da Saude
    data
    """

    query_for_estimated_population = CityData.objects.filter(
        state=row.estado, city=row.municipio
    ).first()
    if query_for_estimated_population:
        estimated_population_2019 = (
            query_for_estimated_population.estimated_population_2019
        )
        city_ibge_code = query_for_estimated_population.city_ibge_code
        if estimated_population_2019:
            # Delete previous data
            query_for_estimated_population.delete()
            print(f"Previou data of {row.estado} - {row.municipio} erased!")
            CityData.objects.create(
                state=row.estado,
                update_source="MS",
                city=row.municipio,
                city_ibge_code=city_ibge_code,
                confirmed=row.casosAcumulado,
                confirmed_per_100k_inhabitants=(
                    (row.casosAcumulado / estimated_population_2019) * 100000
                ),
                date=row.data,
                deaths=row.obitosAcumulado,
                death_rate=row.obitosAcumulado / row.casosAcumulado,
                estimated_population_2019=estimated_population_2019,
            )
    else:
        CityData.objects.create(
            state=row.estado,
            update_source="MS",
            city=row.municipio,
            city_ibge_code=row.codmun,
            confirmed=row.casosAcumulado,
            confirmed_per_100k_inhabitants=(
                (row.casosAcumulado / row.populacaoTCU2019) * 100000
            ),
            date=row.data,
            deaths=row.obitosAcumulado,
            death_rate=row.obitosAcumulado / row.casosAcumulado,
            estimated_population_2019=row.populacaoTCU2019,
        )


def iterate_dataframe_rows_and_save_new_data_in_database(df):
    """
    Iterate dataframe and compare existing data in database
    """
    print("Iterating the dataframe...")
    saving_instances = 0
    for row in df.itertuples():
        # View it later
        # Search brazil data and if empty, save it
        if row.regiao == "Brasil":
            query_brazil = CountryData.objects.filter(
                translated_country_name=row.regiao, date=row.data
            )
            if not query_brazil:
                save_brazil_instance_using_ms_source(row)
        # Search state data and if empty, save it
        elif row.codmun == "0" and row.regiao != "Brasil":
            query_state = StateData.objects.filter(
                state=row.estado, date=row.data
            )
            if not query_state:
                save_state_instance_using_ms_source(row)
                print(f"{row.data} - {row.estado} - Saved to database!")
                saving_instances += 1
            else:
                print(f"{row.data} - {row.estado} - Already in database")
        # Search cities data and if empty, save it
        # elif row.codmun != "0" and row.municipio:
        #     query_city = CityData.objects.filter(
        #         city_ibge_code=row.codmun, date=row.data
        #     )
        #     if not query_city:
        #         save_city_instance_using_ms_source(row)
        #         print(
        #             f"{row.data} - {row.estado} - {row.municipio} - Saved to database!"
        #         )
        #         saving_instances += 1

    # Delete excel file before saving data
    delete_xlsx_files_after_processing()
    if saving_instances > 0:
        return True
    else:
        print("All data is already updated")
        return False


def delete_xlsx_files_after_processing():
    """
    Search for xlsx files in BASE_DIR and delete all of it
    """
    print("Deleting xlsx file...")
    for file in listdir("."):
        if file.endswith("xlsx"):
            remove(file)


def pipeline_to_save_data_using_ms_source():
    """
    Pipeline function to save new data to database using
    Ministerio da Saude source data
    """
    print("Starting the pipeline for MS data...")
    date_today = datetime.date.today()
    yesterday = date_today - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    today = date_today.strftime("%Y-%m-%d")

    # problems with selenium in server
    # xlsx_file = pipeline_to_download_xlsx_file()
    xlsx_file = [
        xlsx_file for xlsx_file in listdir(".") if xlsx_file.endswith("xlsx")
    ]
    xlsx_file = xlsx_file[0]

    df = open_xlsx_file_with_pandas(xlsx_file)
    filtered_df_by_today_date = filter_dataframe_to_find_data_of_specific_date(
        df, today
    )
    cleaned_df = cleanup_dataframe(filtered_df_by_today_date)
    iterate_dataframe_rows_and_save_new_data_in_database(cleaned_df)
