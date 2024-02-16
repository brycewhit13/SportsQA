#Imports
import os
from PyPDF2 import PdfReader

# Constants
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

# Football Classes
class NFL_Football():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nfl_rulebook_2023.pdf')
        self.online_link = 'https://operations.nfl.com/media/tvglh0mx/2023-rulebook_final.pdf'
        self.league_name = 'NFL'
        self.sport_name = 'Football'
        
        
    def load_raw_text(self):
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text