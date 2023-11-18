# Imports
import os
from PyPDF2 import PdfReader

from constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER

# Hockey Classes
class NHL_Hockey():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nhl_rulebook_2023.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'nhl_rulebook_processed')
        self.online_link = 'https://media.nhl.com/site/asset/public/ext/2023-24/2023-24Rulebook.pdf'
        self.league_name = 'NHL'
        self.sport_name = 'Hockey'

    
    def load_raw_text(self):
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text