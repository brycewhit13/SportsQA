# Imports
from enum import Enum

from src.Sports.football import NFL_Football
from src.Sports.hockey import NHL_Hockey
from src.Sports.basketball import NBA_Basketball, WNBA_Basketball
from src.Sports.ultimate import USAU_Ultimate

from .base import BaseSport

# Create Objects to pass into the Enum
NFL_Football = NFL_Football()
NHL_Hockey = NHL_Hockey()
NBA_Basketball = NBA_Basketball()
WNBA_Basketball = WNBA_Basketball()
USAU_Ultimate = USAU_Ultimate()

# Enumeration for the sports - NOTE: This is in this file because it has the same 
#                                    name as the folder and will throw an error if moved elsewhere
class Sports(Enum):
    NFL = NFL_Football
    NHL = NHL_Hockey
    NBA = NBA_Basketball
    WNBA = WNBA_Basketball
    USAU = USAU_Ultimate
    
    def get_object(self):
        return self.value
    
    def get_all_objects():
        return [sport.value for sport in Sports]
    
    def get_name(self):
        return self.name
    
    def get_all_names():
        return [sport.name for sport in Sports]

