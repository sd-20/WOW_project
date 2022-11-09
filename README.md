# Who Owns Whom Project
Text scraping to identify parent companies and subsidiaries in given books (text files), and transferring data into ```.xlsx``` file, using ```python``` and various packages

# Steps

## 1. Installing Python Virtual Environment and Packages

### Prerequisites
- Python version 3.10

This will allow you to install necessary packages and keep them contained in this directory

1. Run ```python -m venv venv``` in the directory of the project to install the venv
2. Then, activate the environment by running ```source venv/bin/activate``` (Mac) or ```venv\Scripts\Activate.ps1``` (Windows)
3. Install dependant packages using ```pip install -r requirements.txt```

## 2. How to Run the Script
1. Open command prompt (windows) or terminal (mac) and navigate to the project directory
2. type  ```python3 scripts.py```
3. Will eventually expand so you can type in file path parameters 

## 3. Results
1. Navigate to the directory of the project
2. Open ```output.xlsx``` in a spreadsheet editor to see results

# Notes
## Week 1
- Some more fine tuning can be done for the rules to improve classification accuracy
- Look into building a machine learning model utilizing classification algorithms 
- Need to incorporate observing multiple lines (how would we feed this in to the model in the future, etc.)
- Having a method of checking country names that are misspelled (whether close enough match to a country) 
- Flag lines that might be mistaken for countries
- Store Parent firm industry names as field (some countries may have multiple separated by ",")
- Store Parent Country
- Sometimes extra characters after country name ("," , "")
- Match accented characters with corresponding origianl (U.S.A with Uaccented.S.A)
- sometimes if country is repeated '