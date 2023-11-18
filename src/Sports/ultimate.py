# Imports
import os
from constants import PROCESSED_DATA_FOLDER

# Ultimate Classes
class USAU_Ultimate():
    
    def __init__(self):
        self.raw_data_path = None
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'usau_rulebook_processed')
        self.online_link = 'https://usaultimate.org/rules/'
        self.league_name = 'USAU'
        self.sport_name = 'Ultimate'