# Imports
import os

from PyPDF2 import PdfReader

from src.Sports.base import BaseSport

# Constants
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

# Hockey Classes
class NHL_Hockey(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nhl_rulebook_2023.pdf'), 
            online_link = 'https://media.nhl.com/site/asset/public/ext/2023-24/2023-24Rulebook.pdf', 
            league_name = 'NHL', 
            sport_name = 'Hockey'
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