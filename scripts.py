import pandas as pd
from countries import get_countries, is_country

# get dictionaries of all countries (current countries, older countries)
countries_dict, countries_dict1 = get_countries()

# function inputs
book = 'books/EUROPE_1980_p3132.txt'
year = 1980
continent = "Europe"
output = 'spreadsheets/output.xlsx'


def book_to_xlsx(book, year, continent, output):
    """
    function to transform a text file into a spreadsheet

    :param book:        path of txt file to read in (ex: 'books/EUROPE_1980_p3132.txt')
    :param year:        year of book
    :param continent:   continent of book
    :param continent:   path of .xlsx file to store output (ex: 'spreadsheets/output.xlsx')
    :return: None       
    """ 

    # list to store each row in the spreadsheet
    rows = []

    with open(book, 'r', errors="ignore", encoding="utf-8") as file:
        for line_id, line in enumerate(file):

            # reinitialize fields at each new line
            d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country = 0, 0, 0, 0, 0
            d_subsidiary_country = ''

            # remove all special characters ('\n', etc.) and white spaces at start & end of line
            stripped_line = line.strip()
            
            # skip stripped line if it is empty
            if len(stripped_line) == 0:
                continue
            
            #  page breaks and lines with 4 characters or less are waste (page numbers, etc. )
            if len(stripped_line) <= 4:
                d_waste = 1
    
            # difference in length from line and line without the left whitespaces gives the indent
            indent = len(line) - len(line.lstrip()) 
            
            # difference in indents from current line and previous line
            prev_diff = indent - (len(rows[-1][3]) - len(rows[-1][3].lstrip())) if line_id >= 1 else 0
            
            # last word in line
            last_word = stripped_line.split()[-1] 
            
            # parent lines have an indent of 0, or end in two letter combos and are all uppercase
            if indent == 0 or (len(last_word) == 2 and (last_word).isupper()):
                d_parent = 1
                if (len(rows) > 0) and (rows[-1][4] == 1):
                    d_parent = 0
                    d_part_prev_line = 1
            elif indent == 2 or prev_diff == 2:
                d_part_prev_line = 1
            elif indent == 3:
                d_subsidiary = 1            
                d_subsidiary_country = last_word if is_country(countries_dict, countries_dict1, last_word) else '' 

            rows.append([continent, year, line_id + 1, line, d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country])
            
    data = pd.DataFrame(rows, columns = ["continent", "year", "line_id", "line_orig", "d_parent", "d_subsidiary", "d_waste", "d_part_prev_line", "d_subsidiary_country"])
    with pd.ExcelWriter(output) as writer:
        data.to_excel(writer)  


book_to_xlsx(book, year, continent, output)







