from thefuzz import fuzz 
import pycountry 

def clean(line):
    return line.replace(',','').replace('.','').replace('\'','').replace('■','').replace('•','').replace('।','').replace(':','').replace('¹','')

def get_indent(line):
    return len(line) - len(line.lstrip())

# create dictionary of country names -> easy lookup of countries 
def get_countries():
    countries_dict = {country.name.upper(): True for country in list(pycountry.countries)}
    missing = ['USA', 'UK', 'VENEZUELA', 'ZAIRE','EIRE', 'W GERMANY', 'IVORY COAST', 'RHODESIA', 'ALGERIA']
    for country in missing:
        countries_dict[country] = True
    for country in list(pycountry.historic_countries): 
        countries_dict[country.name.upper()] = True
    return countries_dict

# match country names with words from end of the line
def country_match(line, countries_dict):
    # cleaned_line = clean_word(line).upper().split()[:-3:-1]
    last_two_words = ' '.join(clean(line).split()[-2::]).upper()   
    last_word = clean(line).split()[-1].upper()
    res = None
    if countries_dict.get(last_two_words) is not None:
        return last_two_words, 100
    elif countries_dict.get(last_word) is not None:
        return last_word, 100   
    for c in countries_dict.keys():
        if len(last_word) != len(c) and len(last_two_words) != len(c): continue
        partial_ratio = fuzz.partial_ratio(last_word, c)
        ratio = max(fuzz.ratio(last_word, c), fuzz.ratio(last_two_words, c))
        if partial_ratio == 100:
            return  c, 100
        elif ratio >= 66:
            if res is None:
                res = c, ratio
            elif ratio > res[1]:
                res = c, ratio            

    return res
