# Imports
import os
import requests

from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from src.constants import ACCEPTABLE_CHARS


# Soccer classes
class FIFA_Soccer(BaseSport):
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'fifa_rulebook_2023_2024.pdf'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'FIFA_processed.txt'),
            online_link = 'https://downloads.theifab.com/downloads/laws-of-the-game-2023-24?l=en', 
            league_name = 'FIFA', 
            sport_name = 'Soccer'
        )
    
    
    def load_raw_text(self):
        """
        Load the raw data and return it as a string
        """
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text

    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = raw_text.replace('’', '\'')
        processed_text = processed_text.replace('‘', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('…', '...')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, ' ')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)


class MLS_Soccer(BaseSport):
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'mls_rulebook_2023_2024.txt'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'MLS_processed.txt'),
            online_link = 'https://www.mlssoccer.com/about/competition-guidelines', 
            league_name = 'MLS', 
            sport_name = 'Soccer'
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
        # Create the raw text file for later
        raw_text = ''

        # Request the webpage
        html = requests.get(self.online_link)

        # Parse the html and save the text
        soup = BeautifulSoup(html.content, 'html.parser')
        
        # Get the main rules
        main_rules = soup.find(name='div', attrs={'class':'oc-c-article__body d3-l-grid--inner'})
        for section in main_rules:
            if section.text not in raw_text:
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