####################################################################
# Filename: generate_data.py                                       #
# Author: Bryce Whitney                                            #
# Last Edit: 3/24/2023                                             #
#                                                                  #
# Description: This script loads the data from the raw_data folder #
# or scrapes it from the web and saves it to the text_data folder. #
####################################################################


# Imports
import os
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
from constants import RAW_DATA_FOLDER_PATH, TEXT_DATA_FOLDER_PATH
from Sport import Sport, get_league

# Functions
def pdf_to_text(filename: str, sport: Sport, start_page: int = 0, end_page: int = None):
    """Loads text from a pdf file and saves it to a txt file. You can specify the start and end pages to load
    and the resulting text is stored in the text_data folder with the output_name as the file name.

    Args:
        filename (str): the filename in the raw data folder
        output_name (str): Output file name
        start_page (int, optional): the first page to load. Defaults to 0.
        end_page (int, optional): the last page to load. Defaults to None.
    """
    # Load the rulebook from the PDF
    data = PdfReader(os.path.join(RAW_DATA_FOLDER_PATH, filename))
    
    # If no end page is specified, use the last page
    # Check to make sure it is valid if it is specified
    if(end_page is None):
        end_page = len(data.pages)
        
    if(end_page > len(data.pages)):
        end_page = len(data.pages)
        
    if(end_page < start_page):
        end_page = start_page
        
    # Extract the test from the rulebook
    text = ""
    for page in range(start_page, end_page):
        text += data.pages[page].extract_text()
    
    # Save to a txt file
    output_name = get_league(sport, lower=True) + '_rules.txt'
    with open(os.path.join(TEXT_DATA_FOLDER_PATH, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

def scrape_ultimate_data(sport: Sport = Sport.ULTIMATE):
    """Scrapes USAU ultimate rules from the website and saves to a txt file
    """
    # Store the url
    url = 'https://usaultimate.org/rules/'
    
    # Scrape the html from the webpage
    html = requests.get(url)
    
    # Parse the html
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all(name='li')[1:]
    
    # Extract the text from the results list
    text = ''
    for result in results:
        text += result.text
    
    # Save to a txt file
    output_name = get_league(sport, lower=True) + '_rules.txt'
    with open(os.path.join(TEXT_DATA_FOLDER_PATH, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

# Main Function
if __name__ == "__main__":
    print("Loading NFL Data...")
    pdf_to_text(filename='2022-nfl-rulebook-final.pdf', sport=Sport.FOOTBALL)
    
    print("Loading NHL Data...")
    pdf_to_text(filename='2022-nhl-rulebook.pdf', sport=Sport.HOCKEY)
    
    print("Loading NBA Data...")
    pdf_to_text(filename='2022-2023-NBA-RULE-BOOK.pdf', sport=Sport.BASKETBALL)
    
    print("Loading WNBA Data...")
    pdf_to_text(filename='2022-WNBA-RULE-BOOK-FINAL.pdf', sport=Sport.WOMENS_BASKETBALL)
    
    print("Loading Cricket Data...")
    pdf_to_text(filename='2020-ICC-Playing-Handbook.pdf', sport=Sport.CRICKET)
    
    print("Loading Ultimate Data...")
    scrape_ultimate_data(sport=Sport.ULTIMATE)