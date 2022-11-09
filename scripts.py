import pandas as pd
from countries import get_countries, is_country

# get dictionaries of all countries (current countries, older countries)
# used to check subsidiary countries (using ISO 3166 standards)
countries_dict, countries_dict1 = get_countries()

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

    with open('books/' + book, 'r', errors="ignore", encoding="utf-8") as file:
        # for each line in the file, get the line index (line_id), and line (line) 
        for line_id, line in enumerate(file):

            # reinitialize fields at each new line
            d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country = 0, 0, 0, 0, 0
            d_subsidiary_country = ''

            # remove all special characters ('\n', etc.) and white spaces at start & end of line
            stripped_line = line.strip()
            
            # skip stripped line if it is empty
            if len(stripped_line) == 0:
                continue
            #  lines with 5 characters or less are waste (page numbers, etc. ) unless previous line is a subsidiary 
            elif len(stripped_line) <= 5:
                if len(rows) > 0 and rows[-1][5] == 1:
                    d_part_prev_line = 1
                else:
                    d_waste = 1
            else:
                # difference in length from line and line without the left whitespaces gives the indent
                indent = len(line) - len(line.lstrip()) 
                
                # difference in indents from current line and previous line
                prev_diff = indent - (len(rows[-1][3]) - len(rows[-1][3].lstrip())) if line_id >= 1 else 0
                
                # first word in line (removing '"')
                first_word = stripped_line.split()[0].replace("\"","")
                # last word in line (removing '.' for countries (ex: U.S.A))                                                                            
                last_word = stripped_line.split()[-1].replace(".","") 
                # check for line ending of previous line (ex: "," indicates this line is part of prev)
                prev_line_end = rows[-1][3].strip().split()[-1][-1] 

                # parent lines have an indent of 0, or end in two letter uppercase combos (ex: SE)
                if indent == 0 and (len(last_word) == 2 and (last_word).isupper()) and first_word.isupper():
                    d_parent = 1
                    # if previous line is a parent, and same indent then current is not, is part of prev
                    if (len(rows) > 0) and (rows[-1][4] == 1):
                        d_parent = 0
                        d_part_prev_line = 1
                # if its an indent of 3 and first word is not uppercase its a subsidiary
                elif indent == 3 or is_country(countries_dict, countries_dict1, last_word):
                    d_subsidiary = 1        
                    d_subsidiary_country = last_word if is_country(countries_dict, countries_dict1, last_word) else ''
                # if indent of 2, or 2 more than the prev line, or prev line ends with ",", it is part of it
                elif indent == 2 or prev_diff == 2 or prev_line_end == ',':
                    d_part_prev_line = 1   
                # if nothing, else, then classify as subsidiary 
                else:
                    d_subsidiary = 1
                
            # add fields to list of rows            
            rows.append([continent, year, line_id + 1, line, d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country])

    # transform rows into a data frame with corresponding columns and write to output xlsx file    
    data = pd.DataFrame(rows, columns = ["continent", "year", "line_id", "line_orig", "d_parent", "d_subsidiary", "d_waste", "d_part_prev_line", "d_subsidiary_country"])
    with pd.ExcelWriter('spreadsheets/' + output) as writer:
        data.to_excel(writer)  








