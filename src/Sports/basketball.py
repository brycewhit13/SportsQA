# imports
import os
from PyPDF2 import PdfReader

from constants import RAW_DATA_FOLDER

# Basketball Classes
class NBA_Basketball():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nba_rulebook_2023.pdf')
        self.online_link = 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf'
        self.league_name = 'NBA'
        self.sport_name = 'Basketball'
        
    
    def load_raw_text(self):   
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text
        

class WNBA_Basketball():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'wnba_rulebook_2022.pdf')
        self.online_link = 'https://cdn.wnba.com/league/2022/05/2022-WNBA-RULE-BOOK-FINAL.pdf'
        self.league_name = 'WNBA'
        self.sport_name = 'Basketball'
    
    
    def load_raw_text(self):
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text