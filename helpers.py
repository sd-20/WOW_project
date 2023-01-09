from thefuzz import fuzz
from unidecode import unidecode 
import pycountry 

def clean(line, allowed={'&':True, ' ':True}):
    res = line
    for char in line:
        if not char.isalpha() and not char.isnumeric() and allowed.get(char) is None:
            res = res.replace(char, '')
    # return line.replace(',','').replace('.','').replace('\'','').replace('■','').replace('•','').replace('।','').replace(':','').replace('¹','')
    return unidecode(res)

def get_indent(line):
    return len(line) - len(line.lstrip())

# create dictionary of country names -> easy lookup of countries 
def get_countries():
    countries_dict = {unidecode(country.name.upper()): True for country in list(pycountry.countries)}
    missing = ['USA', 'UK', 'VENEZUELA', 'ZAIRE','EIRE', 'W GERMANY', 'IVORY COAST', 
                'RHODESIA', 'ALGERIA', 'DUBAI', 'IRAN', 'COLUMBIA', 'TAIWAN', 'POLYNESIA', 
                'ENGLAND', 'CHANNEL ISLANDS', 'WINDWARD ISLANDS', 'VIRGIN ISLANDS', 'WEST GERMANY', 'SYRIA']
    misspelled = ["ARMENIA","AMERICA SAMOA", "SOUTH KOREA"]
    for country in missing:
        countries_dict[country] = True
    for country in list(pycountry.historic_countries): 
        countries_dict[country.name.upper()] = True
    for country in misspelled:
        countries_dict.pop(country, None)

    return countries_dict

def get_iso_codes():
    iso_dict = {unidecode(country.name.upper()): country.numeric for country in list(pycountry.countries)}
    common_miss = ['UK', 'US', 'USA', 'W GERMANY', 'IVORY COAST', 'EIRE', 'VENEZUELA', 'IRAN', 'TAIWAN', 'ENGLAND', 'COLUMBIA', 'WEST GERMANY', 'NETHERLANDS ANTILLES']
    common_miss_match = ['UNITED KINGDOM', 'UNITED STATES', 'UNITED STATES', 'GERMANY', 'COTE D\'IVOIRE', 'IRELAND', 'VENEZUELA, BOLIVARIAN REPUBLIC OF', 'IRAN, ISLAMIC REPUBLIC OF', 'TAIWAN, PROVINCE OF CHINA', 'UNITED KINGDOM', 'COLOMBIA', 'GERMANY', 'NETHERLANDS']
    for missed, matched in zip(common_miss, common_miss_match):
        iso_dict[missed] = iso_dict[matched]
    return iso_dict

# match country names with words from end of the line
def country_match(line, countries_dict):
    cleaned_line = clean(line).split()
    if len(cleaned_line) < 1: return None 
    last_two_words = ' '.join(cleaned_line[-2::]).upper()   
    last_word = cleaned_line[-1].upper()
    res = None
    if countries_dict.get(last_two_words) is not None:
        return last_two_words, 100, ""
    elif countries_dict.get(last_word) is not None:
        return last_word, 100, ""   
    common_misses = ["AMERICA", "LIBRARY", "LOAN", "CIE", "GESTION", 
                    "FINANCE", "AFRICA", "ASIA", "WESTERN", "ALABAMA", 
                    "CLUB", "CORP", "CO", "INC", "LATINA", "DENISON", "CIA", "JERSEY"]

    if last_word in common_misses:
        return None
    partial_match = ""
    full_match = ""
    for c in countries_dict.keys():
        if len(last_word) != len(c) and len(last_two_words) != len(c): 
            continue
        if fuzz.partial_ratio(last_word, c) > fuzz.partial_ratio(last_two_words, c):
            partial_ratio = fuzz.partial_ratio(last_word, c)
            partial_match =  last_word
        else :
            partial_ratio = fuzz.partial_ratio(last_two_words, c)
            partial_match =  last_two_words
        if fuzz.ratio(last_word, c) > fuzz.ratio(last_two_words, c):
            ratio = fuzz.ratio(last_word, c)
            full_match =  last_word
        else :
            ratio = fuzz.ratio(last_two_words, c)
            full_match =  last_two_words
        if partial_ratio == 100 and ratio >= 71:
            return  c, 100, partial_match
        elif ratio >= 71:
            if res is None:
                res = c, ratio, full_match
            elif ratio > res[1]:
                res = c, ratio, full_match            

    return res

# gets 2-digit uppercase letter industry codes
def get_industry(word):
    res = ''
    for i in range(0,len(word), 2):
        res += word[i:i+2] + ','
    return res[:-1]

# gets 4-digit numeric industry codes  
def get_industry_numeric(word):
    res = ''
    for i in range(0,len(word), 4):
        res += word[i:i+4] + ','
    return res[:-1]

# count of upper case letters in line
def num_upper(line):
    count = 0
    for c in line:
        if c.isupper():
            count += 1
    return count 

# count of numeric digits in line
def num_digits(line):
    count = 0
    for c in line:
        if c.isnumeric():
            count += 1
    return count 