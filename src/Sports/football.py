#Imports
import os

from PyPDF2 import PdfReader

from src.Sports.base import BaseSport
#from src.Sports import BaseSport

# Constants
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

# Football Classes
class NFL_Football(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nfl_rulebook_2023.pdf'), 
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