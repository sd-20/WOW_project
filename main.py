from scripts import book_to_xlsx
import datetime
import time

books = ['WOW_EUROPE_1980.txt','wow_1980_1981_na.txt','wow_1984_na.txt','wow_1997_na_2.txt']
years = [1980, 1981, 1984, 1997]
continents = ['Europe','NA', 'NA','NA']
outputs = ['WOW_EUROPE_1980.xlsx','wow_1980_1981_na.xlsx','wow_1984_na.xlsx','wow_1997_na_2.xlsx']

for i in range(1,2):
    start_time = time.time()
    book_to_xlsx(books[i], years[i], continents[i], outputs[i])
    runtime = str(datetime.timedelta(seconds=time.time() - start_time))
    print(f"|--- runtime---|: {runtime} for {books[i]}")
