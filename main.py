from scripts import *
import datetime
import time
from helpers import get_countries, get_iso_codes
import os

books = os.listdir('C:\\Users\samue\\OneDrive\Desktop\WOW_project\\books')
runtimes = []

# dictionary of all countries (current countries, older countries)
countries_dict = get_countries()
#  dictionary of countries and their ISO 3166 codes 
iso_dict = get_iso_codes()

# testing different lines...
# line = "CBS SCHALLPLATTEN GMBH. A-1031 Wien,  SE"
# print(test_line(line, countries_dict, iso_dict, []))

for book in books:
    start_time = time.time()
    book_to_xlsx(book, book + '.xlsx', countries_dict, iso_dict)
    runtime = str(datetime.timedelta(seconds=time.time() - start_time))
    print(f"|--- runtime---|: {runtime} for {book}")
    runtimes.append(book + ': ' + runtime)

# write runtime for each file 
with open('runtimes.txt', 'w') as f:
    f.write('\n'.join(runtimes))
