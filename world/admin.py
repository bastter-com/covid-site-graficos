# from django.contrib import admin
# from .models import WorldTotalData, CountryData
# from .views import get_data_for_table, push_each_missing_data_to_countrydata_table


# class CountryDataAdmin(admin.ModelAdmin):
#     def push_several_missing_data_to_countrydata_table(self, request, num_of_countries):
#         table_data = get_data_for_table()
#         world_table_data = table_data[0]
#         first_twenty_countries = world_table_data[:20]
#         for country in first_twenty_countries:
#             country_name = country["country"]
#             push_each_missing_data_to_countrydata_table(country_name)


# admin.site.register(WorldTotalData)
# admin.site.register(CountryData, CountryDataAdmin)
