# imports
import os
from PyPDF2 import PdfReader

from constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from constants import ACCEPTABLE_CHARS

# Basketball Classes
class NBA_Basketball():
    
    def __init__(self):
        self.online_link = 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf'
        self.league_name = 'NBA'
        self.sport_name = 'Basketball'
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nba_rulebook_2023.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, f'{self.league_name}_processed.txt')
        
    
    def load_raw_text(self):   
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
        
        # Remove any spots with more than one space
        processed_text = ' '.join(raw_text.split())
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = processed_text.replace('’', '\'')
        processed_text = processed_text.replace('‘', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('°', ' degrees') # Degree symbol
        
        # Replace fractions
        processed_text = processed_text.replace('¾', '3/4')
        processed_text = processed_text.replace('½', '1/2')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, '')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)

class WNBA_Basketball():
    
    def __init__(self):
        self.online_link = 'https://cdn.wnba.com/league/2022/05/2022-WNBA-RULE-BOOK-FINAL.pdf'
        self.league_name = 'WNBA'
        self.sport_name = 'Basketball'
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'wnba_rulebook_2022.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, f'{self.league_name}_processed.txt')
    
    
    def load_raw_text(self):
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
        
        # Remove any spots with more than one space
        processed_text = ' '.join(raw_text.split())
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = processed_text.replace('’', '\'')
        processed_text = processed_text.replace('‘', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, '')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)