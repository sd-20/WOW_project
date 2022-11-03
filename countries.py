import pycountry 

# create dictionary of country names -> easy lookup of countries 
def get_countries():
    # stores all current countries
    countries_dict = {country.name: True for country in list(pycountry.countries)}
    # stores older countries like Yugoslavia
    countries_dict1 = {country.name: True for country in list(pycountry.historic_countries)} 
    return countries_dict, countries_dict1

# checks if a country is in two given dictionaries (ex: countries_dict["USA"] == 1 means USA is a country)
def is_country(countries_dict, countries_dict1, country):
    return countries_dict.get(country) is not None or countries_dict1.get(country) is not None
