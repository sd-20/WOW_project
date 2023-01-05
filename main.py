from scripts import book_to_xlsx
import datetime
import time
from unidecode import unidecode
from helpers import *
import os

books = os.listdir('C:\\Users\samue\\OneDrive\Desktop\WOW_project\\books')
runtimes = []

print("hi")
# for book in books:
#     start_time = time.time()
#     book_to_xlsx(book, book + '.xlsx')
#     runtime = str(datetime.timedelta(seconds=time.time() - start_time))
#     print(f"|--- runtime---|: {runtime} for {book}")
#     runtimes.append(book + ': ' + runtime)

# # # write runtime for each file 
# with open('runtimes.txt', 'w') as f:
#     f.write('\n'.join(runtimes))
