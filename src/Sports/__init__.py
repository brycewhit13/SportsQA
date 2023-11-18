# Imports
from enum import Enum

from Sports.football import NFL_Football
from Sports.hockey import NHL_Hockey
from Sports.basketball import NBA_Basketball, WNBA_Basketball
from Sports.ultimate import USAU_Ultimate

# Create Objects to pass into the Enum
NFL_Football = NFL_Football()
NHL_Hockey = NHL_Hockey()
NBA_Basketball = NBA_Basketball()
WNBA_Basketball = WNBA_Basketball()
USAU_Ultimate = USAU_Ultimate()

# Enumeration for the sports
class Sport(Enum):
    NFL = NFL_Football
    NHL = NHL_Hockey
    NBA = NBA_Basketball
    WNBA = WNBA_Basketball
    USAU = USAU_Ultimate