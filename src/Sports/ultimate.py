# Imports
import os
import requests

from bs4 import BeautifulSoup
from langchain_community.document_loaders import TextLoader

from constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from constants import ACCEPTABLE_CHARS

# Ultimate Classes
class USAU_Ultimate():
    
    def __init__(self):
        self.online_link = 'https://usaultimate.org/rules/'
        self.league_name = 'USAU'
        self.sport_name = 'Ultimate'
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'usau_rulebook_2024.txt')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, f'{self.league_name}_processed.txt')
        
    
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
    
    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Remove any spots with more than one space
        processed_text = ' '.join(raw_text.split())
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = processed_text.replace('’', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('…', '...')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, '')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)
    
    
    def load_processed_text(self):
        pass