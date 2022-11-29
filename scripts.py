import pandas as pd
from helpers import get_indent, get_countries, country_match, clean

def book_to_xlsx(book, year, continent, output):
    """
    function to transform a text file into a spreadsheet

    :param book:        path of txt file to read in (ex: 'books/EUROPE_1980_p3132.txt')
    :param year:        year of book
    :param continent:   continent of book
    :param continent:   path of .xlsx file to store output (ex: 'spreadsheets/output.xlsx')
    :return: None       
    """ 

    # get dictionaries of all countries (current countries, older countries)
    # used to check subsidiary countries (using ISO 3166 standards)
    countries_dict = get_countries()
    country_counts = {}
    
    # list to store each row in the spreadsheet
    rows = []
    cleaned_lines = []

    with open('books/' + book, 'r', errors="ignore", encoding="utf-8") as file:
        # for each line in the file, get the line index (line_id), and line (line)
        alpha, industry = '','' 
        prev_indent = 0

        for line_id, line in enumerate(file):
           
            d_parent, d_subsidiary, d_waste, d_part_prev_line, d_country_match = 0, 0, 0, 0, 0
            d_subsidiary_country = ''
            # remove all special characters ('\n', etc.) and white spaces at start & end of line
            stripped_line = line.strip()
            words = stripped_line.split()

            # skip stripped line if it is empty
            if len(stripped_line) == 0:
                continue
            #  lines with 5 characters or less are waste (page numbers, etc.) unless previous line is a subsidiary or country (continuation)
            elif len(stripped_line) <= 5 or len(words) <= 1:
                if len(rows) > 0:
                    if rows[-1][5] == 1 or rows[-1][4] == 1:
                        d_part_prev_line = 1
                else:
                    d_waste = 1
            else:
                indent = get_indent(line)
                prev_diff = indent - (prev_indent) if line_id >= 1 else 0                                                   # difference in indents from current line and previous line                                                                                      
                last_word = clean(words[-1])                                       # last word in line (removing '.' and ',' for countries (ex: U.S.A) and multiple industries)                                                                            
                prev_line_end = rows[-1][3].strip().split()[-1][-1]                                                         # check for line ending of previous line (ex: "," indicates this line is part of prev)
                prev_indent = indent

                # parent lines have an indent of 0, or end in two/four letter industry combos (ex: SE or SE,EX)
                if (indent == 0 
                    and (((len(last_word) == 2 or len(last_word) == 4) 
                    and (((last_word).isupper() and (last_word.isalpha())) 
                    or last_word.isnumeric()))
                    )):
                    d_parent = 1
                
                    industry = last_word if len(last_word) == 2 else ','.join([last_word[0:2], last_word[2:]])
                    # if previous line is a parent, and same indent then current is not, is part of prev
                    if (len(rows) > 0) and (rows[-1][4] == 1):
                        d_parent = 0
                        d_part_prev_line = 1
                # lines with indent of 3, or same indent as previous, or ending with country names are subsidiary
                elif (indent == 3 
                    or (prev_diff == 0 and rows[-1][4] == 0)
                    or prev_diff == 4
                    or country_match(stripped_line, countries_dict)
                    ):
                    d_subsidiary = 1
                    if country_match(stripped_line, countries_dict):
                        d_subsidiary_country, d_country_match = country_match(stripped_line, countries_dict)
                        if country_counts.get(d_subsidiary_country) is not None:
                            country_counts[d_subsidiary_country][1] = (country_counts[d_subsidiary_country][1]*country_counts[d_subsidiary_country][0] + d_country_match)/(country_counts[d_subsidiary_country][0]+1)  
                            country_counts[d_subsidiary_country][0] += 1
                        else:
                            country_counts[d_subsidiary_country] = [1, d_country_match]

                # if indent of 2, or 2 more than the prev line, or prev line ends with ",", it is part of it
                elif indent == 2 or prev_diff <= 2 or prev_line_end == ',':
                    d_part_prev_line = 1   
                # if nothing, else, then classify as subsidiary 
                else:
                    d_subsidiary = 1
                
            # add fields to list of rows            
            rows.append([continent, year, line_id + 1, line, d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country, d_country_match, industry])
            cleaned_lines.append([line_id + 1, stripped_line])

    # transform rows into a data frame with corresponding columns and write to output xlsx file    
    book_data = pd.DataFrame(rows, columns = ["continent", "year", "line_id", "line_orig", "d_parent", "d_subsidiary", "d_waste", "d_part_prev_line", "d_subsidiary_country", "d_country_match", "industry"])
    cleaned_lines_data = pd.DataFrame(cleaned_lines, columns = ["line_id", "line (cleaned)"])
    countries_data = pd.DataFrame([list(country_counts.keys()), list(c[0] for c in country_counts.values()), list(c[1] for c in country_counts.values())]).T
    countries_data.columns = ['Country', 'Counts', 'Accuracy']
    with pd.ExcelWriter('spreadsheets/' + output) as writer:
        book_data.to_excel(writer, sheet_name = 'book data')  
        cleaned_lines_data.to_excel(writer, sheet_name = 'cleaned lines')  
        (countries_data).to_excel(writer, sheet_name = 'country data')





