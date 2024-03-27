# Imports
import os

from PyPDF2 import PdfReader

from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER
from src.constants import ACCEPTABLE_CHARS

# Golf classes
class PGA_Golf(BaseSport):
    def __init__(self):
            # Call the parent class with these values
            super().__init__(
                raw_data_path = os.path.join(RAW_DATA_FOLDER, 'pga_rulebook_2024.pdf'),
                processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'PGA_processed.txt'),
                online_link = 'https://qualifying.pgatourhq.com/static-assets/uploads/2024-PGA-TOUR-Champions-Player-Handbook-1-4-24.pdf', 
                league_name = 'PGA', 
                sport_name = 'Golf'
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
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('…', '...')
        processed_text = processed_text.replace('⁄', '/')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, '')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)