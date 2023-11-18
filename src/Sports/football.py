#Imports
import os
from constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER

# Football Classes
class NFL_Football():
    
    def __init__(self):
        self.raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nfl_rulebook_2023.pdf')
        self.processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'nfl_rulebook_processed')
        self.online_link = 'https://operations.nfl.com/media/tvglh0mx/2023-rulebook_final.pdf'
        self.league_name = 'NFL'
        self.sport_name = 'Football'