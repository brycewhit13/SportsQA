# Imports
import os
import requests
from bs4 import BeautifulSoup

from constants import PROCESSED_DATA_FOLDER

# Ultimate Classes
class USAU_Ultimate():
    
    def __init__(self):
        self.raw_data_path = None
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'usau_rulebook_processed')
        self.online_link = 'https://usaultimate.org/rules/'
        self.league_name = 'USAU'
        self.sport_name = 'Ultimate'
        
    
    def load_raw_text(self):
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
       
        return raw_text