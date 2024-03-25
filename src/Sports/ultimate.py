# Imports
import os
import requests

from bs4 import BeautifulSoup

from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from src.constants import ACCEPTABLE_CHARS

# Ultimate Classes
class USAU_Ultimate(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'usau_rulebook_2024.txt'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'USAU_processed.txt'),
            online_link = 'https://usaultimate.org/rules/', 
            league_name = 'USAU', 
            sport_name = 'Ultimate Frisbee'
        )
    
    
    def load_raw_text(self):
        """
        Loads the raw text and returns it as a string
        """
        try:
            with open(self.raw_data_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print('File not found, scraping data from the web')
            # Scrape the data from the web
            raw_text = self.scrape_data()
            
            # Save the raw text to a file before returning it
            with open(self.raw_data_path, 'w') as f:
                f.write(raw_text)
            return raw_text
    
    
    def scrape_data(self):
        """
        Scrapes the rules from the web and returns them as a string
        """
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
        
        return raw_text
    
    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = raw_text.replace('’', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('…', '...')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, ' ')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)
