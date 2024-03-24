#Imports
import os

from PyPDF2 import PdfReader

from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from src.constants import ACCEPTABLE_CHARS

# Football Classes
class NFL_Football(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nfl_rulebook_2023.pdf'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'NFL_processed.txt'),
            online_link = 'https://operations.nfl.com/media/tvglh0mx/2023-rulebook_final.pdf', 
            league_name = 'NFL', 
            sport_name = 'Football'
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
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('…', '...')
        
        # Replace fractions
        processed_text = processed_text.replace('¼', '1/4')
        processed_text = processed_text.replace('¾', '3/4')
        processed_text = processed_text.replace('½', '1/2')
        processed_text = processed_text.replace('⅜', '3/8')
        processed_text = processed_text.replace('⅝', '5/8')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, ' ')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)