# Imports
import os
import requests
from bs4 import BeautifulSoup

# Constants
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

# Ultimate Classes
class USAU_Ultimate():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'usau_rulebook_2024.txt')
        self.online_link = 'https://usaultimate.org/rules/'
        self.league_name = 'USAU'
        self.sport_name = 'Ultimate'
        
    
    def load_raw_text(self):
        # Check if the file exists
        if os.path.exists(self.raw_data_path):
            with open(self.raw_data_path, 'r') as f:
                return f.read()

        # Otherwise scrape it from the website
        else:
            # Create the raw text file for later
            raw_text = ''

            # Request the webpage
            html = requests.get(self.online_link)

            # Parse the html and save the text
            soup = BeautifulSoup(html.content, 'html.parser')
            
            # Get the main rules
            main_rules = soup.find(name='ol', attrs={'class':'main-rules'}).find_all(name='li')
            for section in main_rules:
                raw_text += section.text
                
            # Get the appendices
            appendices = soup.find(name='ol', attrs={'class':'appendices'}).find_all(name='li')
            for section in appendices:
                raw_text += section.text

            # Save and return the text
            with open(self.raw_data_path, 'w') as f:
                f.write(raw_text)
            return raw_text