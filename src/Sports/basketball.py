# imports
import os

from PyPDF2 import PdfReader

from src.Sports.base import BaseSport

# Constants
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

# Basketball Classes
class NBA_Basketball(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nba_rulebook_2023.pdf'), 
            online_link = 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf', 
            league_name = 'NBA', 
            sport_name = 'Basketball'
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
        

class WNBA_Basketball(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'wnba_rulebook_2022.pdf'), 
            online_link = 'https://cdn.wnba.com/league/2022/05/2022-WNBA-RULE-BOOK-FINAL.pdf', 
            league_name = 'WNBA', 
            sport_name = 'Basketball'
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