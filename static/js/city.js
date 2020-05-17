$(document).ready(function () {
  $('select#select-uf').change(function () {
    let optionStateSelected = $(this).find('option:selected');
    let stateSelected = optionStateSelected.text();

    let dataToAjax = { uf: stateSelected };
    $.ajax({
      url: '/cidades_detalhe',
      type: 'GET',
      dataType: 'json',
      data: dataToAjax,
      contentType: 'application/json',
      success: function (result) {
        $('#select-city option').remove();
        for (let i = 0; i < result.length; i++) {
          $('#select-city').append(
            '<option class="form-control">' + result[i].name + '</option>'
          );
        }
      },
    });
  });
  $('#search-city-btn').click(function () {
    let optionCitySelected = $('select#select-city').find('option:selected');
    let citySelected = optionCitySelected.text();
    let optionStateSelected = $('select#select-uf').find('option:selected');
    let stateSelected = optionStateSelected.text();
    let dataToAjaxCity = { uf: stateSelected, city: citySelected };
    $.ajax({
      url: '/cidades_dados',
      type: 'GET',
      dataType: 'json',
      data: dataToAjaxCity,
      contentType: 'application/json',
      success: function (result) {
        console.log(result.city);
        $('#city-data-name').text(result.city);
        $('#city-data-name-uf').text(result.uf);
        $('#city-data-confirmed').text(result.confirmed);
        $('#city-data-confirmed-rate').text(
          `${result.cases_rate_per_inhabitants} %`.replace('.', ',')
        );
        $('#city-data-deaths').text(result.deaths);
        $('#city-data-deaths-rate').text(
          `${result.deaths_rate_per_inhabitants} %`.replace('.', ',')
        );
        $('#city-data-date').text(result.date);
        $('#city-data-estimated-population').text(
          `${result.estimated_population_2019}`.replace(
            /\B(?=(\d{3})+(?!\d))/g,
            '.'
          )
        );
      },
    });
  });
});
