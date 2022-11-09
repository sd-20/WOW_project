import pandas as pd
from countries import get_countries, is_country
from scripts import book_to_xlsx

countries_dict, countries_dict1 = get_countries()

books = ['WOW_EUROPE_1980.txt','wow_1980_1981_na.txt','wow_1984_na.txt','wow_1997_na_2.txt']
years = [1980, 1981, 1984, 1997]
continents = ['Europe','NA', 'NA','NA']
outputs = ['WOW_EUROPE_1980.xlsx','wow_1980_1981_na.xlsx','wow_1984_na.xlsx','wow_1997_na_2.xlsx']

for i in range(4):
    book_to_xlsx(books[i], years[i], continents[i], outputs[i])