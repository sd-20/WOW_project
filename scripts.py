import pandas as pd

# Initializing all the field names
continent = "Europe"
year = 1980
d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country = 0, 0, 0, 0, 0
d_subsidiary_country = ''

# list to store each row in the spreadsheet
rows = []

with open('EUROPE_1980_p3132.txt', 'r') as file:
    for line_id, line in enumerate(file):
        # remove all special characters ('\n', etc.) and white spaces at end of line
        stripped_line = line.strip()
        
        # skip stripped line if it is empty
        if len(stripped_line) == 0:
            continue
        
        # # page breaks and lines with 4 characters or less are waste
        # if len(stripped_line) <= 4:
        #     d_waste = 1
 
        # difference in length from line and line without white spaces/special
        # chars at the end (right side) is number of spaces at the front  
        indent = len(line.rstrip()) - len(stripped_line) 
        prev_diff = len(line.rstrip()) - (rows[-1][3]).rstrip() if line_id > 1 else 0
        
        if indent == 2 or prev_diff == 2:
            d_part_prev_line = 1
        elif indent == 3:
            d_subsidiary = 1            
            

        #  break up line into list of words, with " " delimiter
        words = stripped_line.split()
        
        # if last word in line is uppercase and two letters
        # they denote industry and the line is a parent 
        if len(words[-1]) == 2 and (words[-1]).isupper():
            d_parent = 1


        # if len(words[-1]) == 2:
            # curr_parent = 
        
        rows.append([continent, year, line_id, line, d_parent, d_subsidiary, d_waste, d_part_prev_line, d_subsidiary_country])
        
data = pd.DataFrame(rows, columns = ["continent", "year", "line_id", "line_orig", "d_parent", "d_subsidiary", "d_waste", "d_part_prev_line", "d_subsidiary_country"])
data.to_excel("output.xslx")



# ·       Parent names are in ALL CAPITAL LETTERS, subsidiaries are not.

# ·       Parent name lines end in a 2-capital-letter combination (indicating industry). I will provide a list of industry 2-letter combinations on box later on—later books also use 2-digit or 4-digit numeric industry classifications.

# ·       Parent name lines, once they get to the address of the parent, contain some numbers—the vast majority of subsidiary names does not contain numbers.

# ·       Parent names are alphabetical (with few exceptions, and as long as the OCR software did not misread).

# ·       Subsidiary lines often end in company types such as ‘mbH’, ‘GmbH’, or in ‘(A)’.

