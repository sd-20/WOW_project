import pandas as pd
from helpers import *

def book_to_xlsx(book, output, countries_dict, iso_dict):
    """
    function to transform a text file into a spreadsheet

    :param book:        path of txt file to read in (ex: 'books/EUROPE_1980_p3132.txt')
    :param year:        year of book
    :param continent:   continent of book
    :param output:   path of .xlsx file to store output (ex: 'spreadsheets/output.xlsx')
    :return: None       
    """ 

    country_counts = {}
    rows = []
    cleaned_lines = []
    partial_matches = []

    with open('books/' + book, 'r', errors="ignore", encoding="utf-8") as file:
        # for each line in the file, get the line index (line_id), and line (line)
        industry = '' 
        prev_indent = 0

        for line_id, line in enumerate(file):
           
            d_parent, d_subsidiary, d_waste, d_part_prev_line, d_country_match, d_match, d_parent_through_10char, d_part_prev_line_through_num = 0, 0, 0, 0, 0, 0, 0, 0
            d_subsidiary_country, d_iso = '', ''
            # remove all special characters ('\n', etc.) and white spaces at start & end of line
            stripped_line = line.strip()
            words = stripped_line.split()

            # skip stripped line if it is empty
            if len(stripped_line) == 0:
                continue
            elif len(stripped_line) <= 3 or len(words) <= 1:
                d_waste = 1
            #  lines with 5 characters or less are waste (page numbers, etc.) unless previous line is a subsidiary or country (continuation)
            elif len(stripped_line) <= 5 or len(words) <= 1 :
                if len(rows) > 0:
                    if rows[-1][5] == 1 or rows[-1][4] == 1:
                        d_part_prev_line = 1
            else:
                indent = get_indent(line)
                prev_diff = indent - (prev_indent) if line_id >= 1 else 0                                                   # difference in indents from current line and previous line                                                                                      
                last_word = clean(words[-1])                                       # last word in line (removing '.' and ',' for countries (ex: U.S.A) and multiple industries)                                                                            
                last_two_words = clean(words[-2]) + clean(words[-1])
                prev_line_end = str(rows[-1][3]).strip().split()[-1][-1]                                                         # check for line ending of previous line (ex: "," indicates this line is part of prev)
                prev_indent = indent
                chars = stripped_line.replace(" ","")

                # parent lines have an indent of 0, or end in two/four letter industry combos (ex: SE or SE,EX)
                if (indent <= 8 
                    and prev_diff <= 0
                    and len(words) > 2
                    and (((len(last_word) % 2 == 0)  
                    and (((last_word).isupper() and (last_word.isalpha())) 
                    and countries_dict.get(last_word) is None
                    or last_word.isnumeric()))
                    )):
                    d_parent = 1
                    if last_word.isnumeric():
                        if last_two_words.isnumeric():
                            industry = get_industry_numeric(last_two_words)
                        industry = get_industry_numeric(last_word)
                    else:
                        industry = get_industry(last_word)
                    # if previous line is a parent, and same indent then current is not, is part of prev
                    # if (len(rows) > 0) and (rows[-1][4] == 1):
                    #     d_parent = 0
                    #     d_part_prev_line = 1
                elif len(chars) >= 10 and num_upper(chars[:10]) >= 9:
                    d_parent = 1
                    d_parent_through_10char = 1
                # lines with indent of 3, or same indent as previous, or ending with country names are subsidiary
                elif (indent == 3 
                    or (prev_diff == 0 and rows[-1][4] == 0)
                    or prev_diff == 4
                    or country_match(stripped_line, countries_dict)
                    ):
                    d_subsidiary = 1
                    if country_match(stripped_line, countries_dict):
                        # put iso in country match CHANGE
                        d_subsidiary_country, d_country_match, d_match = country_match(stripped_line, countries_dict)
                        d_iso = iso_dict[d_subsidiary_country] if iso_dict.get(d_subsidiary_country) is not None else 'Unknown'

                        if country_counts.get(d_subsidiary_country) is not None:
                            country_counts[d_subsidiary_country][1] = (country_counts[d_subsidiary_country][1]*country_counts[d_subsidiary_country][0] + d_country_match)/(country_counts[d_subsidiary_country][0]+1)  
                            country_counts[d_subsidiary_country][0] += 1
                        else:
                            country_counts[d_subsidiary_country] = [1, d_country_match]
                            
                        if d_country_match < 100:
                            partial_matches.append([line_id + 1, clean(stripped_line), d_match, d_subsidiary_country, d_country_match])

                # if indent of 2, or 2 more than the prev line, or prev line ends with ",", it is part of it
                elif indent == 2 or prev_diff <= 2 or prev_line_end == ',':
                    d_part_prev_line = 1   
                # if a line contains >=2 numbers (0...9) and the previous line is a parent line, it is part of prev
                elif num_digits(chars) >= 2 and len(rows) > 0 and rows[-1][2] == 1:
                    d_part_prev_line_through_num = 1
                    d_part_prev_line = 1
                # if nothing, else, then classify as subsidiary 
                else:
                    d_subsidiary = 1
            
            # add fields to list of rows            
            rows.append([line_id + 1, line, d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country, d_country_match, d_iso, industry, d_parent_through_10char, d_part_prev_line_through_num])
            cleaned_lines.append([line_id + 1, clean(stripped_line)])

    # transform rows into a data frame with corresponding columns and write to output xlsx file    
    book_data = pd.DataFrame(rows, columns = ["line_id", "line_orig", "d_parent", "d_subsidiary", "d_waste", "d_part_prev_line", "d_subsidiary_country", "d_country_match", "d_iso", "industry", "d_parent_through_10char", "d_part_prev_line_through_num"])
    cleaned_lines_data = pd.DataFrame(cleaned_lines, columns = ["line_id", "line (cleaned)"])
    countries_data = pd.DataFrame([list(country_counts.keys()), list(c[0] for c in country_counts.values()), list(c[1] for c in country_counts.values())]).T
    countries_data.columns = ['Country', 'Counts', 'Accuracy']
    partial_country_matches = pd.DataFrame(partial_matches, columns = ["line_id", "line", "match", "match country","score"])
    with pd.ExcelWriter('spreadsheets/' + output) as writer:
        book_data.to_excel(writer, sheet_name = 'book data')  
        cleaned_lines_data.to_excel(writer, sheet_name = 'cleaned lines')  
        (countries_data).to_excel(writer, sheet_name = 'country data')
        partial_country_matches.to_excel(writer, sheet_name= 'partial country matches')


def test_line(line, countries_dict, iso_dict, rows):

    d_parent, d_subsidiary, d_waste, d_part_prev_line, d_country_match, d_match, d_parent_through_10char, d_part_prev_line_through_num = 0, 0, 0, 0, 0, 0, 0, 0
    d_subsidiary_country, d_iso, industry = '', '', ''
    line_id = 1 if len(rows) == 0 else len(rows)
    prev_indent = 0

    # remove all special characters ('\n', etc.) and white spaces at start & end of line
    stripped_line = line.strip()
    words = stripped_line.split()
    # skip stripped line if it is empty
    if len(stripped_line) == 0:
        return 
    elif len(stripped_line) <= 3 or len(words) <= 1:
        d_waste = 1
    #  lines with 5 characters or less are waste (page numbers, etc.) unless previous line is a subsidiary or country (continuation)
    elif len(stripped_line) <= 5 or len(words) <= 1 :
        if len(rows) > 0:
            if rows[-1][5] == 1 or rows[-1][4] == 1:
                d_part_prev_line = 1
    else:
        indent = get_indent(line)
        prev_diff = indent - (prev_indent) if line_id >= 1 else 0                                                   # difference in indents from current line and previous line                                                                                      
        last_word = clean(words[-1])                                       # last word in line (removing '.' and ',' for countries (ex: U.S.A) and multiple industries)                                                                            
        last_two_words = clean(words[-2]) + clean(words[-1])
        prev_line_end = str(rows[-1][3]).strip().split()[-1][-1] if len(rows) > 0 else "" # check for line ending of previous line (ex: "," indicates this line is part of prev)
        prev_indent = indent
        chars = stripped_line.replace(" ","")
        # parent lines have an indent of 0, or end in two/four letter industry combos (ex: SE or SE,EX)
        if (indent <= 8 
            and prev_diff <= 0
            and len(words) > 2
            and (((len(last_word) % 2 == 0)  
            and (((last_word).isupper() and (last_word.isalpha())) 
            and countries_dict.get(last_word) is None
            or last_word.isnumeric()))
            )):
            d_parent = 1

            if last_word.isnumeric():
                if last_two_words.isnumeric():
                    industry = get_industry_numeric(last_two_words)
                else:
                    industry = get_industry_numeric(last_word)
            else:
                industry = get_industry(last_word)
            # if previous line is a parent, and same indent then current is not, is part of prev
            if (len(rows) > 0) and (rows[-1][4] == 1):
                d_parent = 0
                d_part_prev_line = 1
        elif len(chars) >= 10 and num_upper(chars[:10]) >= 9:
            d_parent = 1
            d_parent_through_10char = 1
        # lines with indent of 3, or same indent as previous, or ending with country names are subsidiary
        elif (indent == 3 
            or (prev_diff == 0 and rows[-1][4] == 0)
            or prev_diff == 4
            or country_match(stripped_line, countries_dict)
            ):
            d_subsidiary = 1
            if country_match(stripped_line, countries_dict):
                # put iso in country match CHANGE
                d_subsidiary_country, d_country_match, d_match = country_match(stripped_line, countries_dict)
                d_iso = iso_dict[d_subsidiary_country] if iso_dict.get(d_subsidiary_country) is not None else 'Unknown'
        # if indent of 2, or 2 more than the prev line, or prev line ends with ",", it is part of it
        elif indent == 2 or prev_diff <= 2 or prev_line_end == ',':
            d_part_prev_line = 1   
        # if a line contains >=2 numbers (0...9) and the previous line is a parent line, it is part of prev
        elif num_digits(chars) >= 2 and len(rows) > 0 and rows[-1][2] == 1:
            d_part_prev_line_through_num = 1
            d_part_prev_line = 1
        # if nothing, else, then classify as subsidiary 
        else:
            d_subsidiary = 1

    # print(industry)
    print(d_parent, d_subsidiary, d_waste, d_part_prev_line, d_country_match, d_match, d_parent_through_10char, d_part_prev_line_through_num, d_subsidiary_country, d_iso, sep=', ')

