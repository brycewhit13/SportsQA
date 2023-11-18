# imports
import os
from constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER

# Basketball Classes
class NBA_Basketball():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nba_rulebook_2023.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'nba_rulebook_processed')
        self.online_link = 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf'
        self.league_name = 'NBA'
        self.sport_name = 'Basketball'
        

class WNBA_Basketball():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'wnba_rulebook_2022.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'wnba_rulebook_processed')
        self.online_link = 'https://cdn.wnba.com/league/2022/05/2022-WNBA-RULE-BOOK-FINAL.pdf'
        self.league_name = 'WNBA'
        self.sport_name = 'Basketball'