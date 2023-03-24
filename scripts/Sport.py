#############################################################################
# Filename: Sport.py                                                        #
# Author: Bryce Whitney                                                     #
# Last Edit: 3/24/2023                                                      #
#                                                                           #
# Description: A file containing definitions and methods for the Sport enum #
#############################################################################

# Imports
from enum import Enum

# Sport Enum
class Sport(Enum):
    FOOTBALL = 'Football'
    HOCKEY = 'Hockey'
    BASKETBALL = 'Basketball'
    WOMENS_BASKETBALL = 'Womens Basketball'
    CRICKET = 'Cricket'
    ULTIMATE = 'Ultimate'
    

def get_league(sport: Sport, lower: bool = True):
    """Gets the league for the given sport

    Args:
        sport (Sport): The sport to get the league for

    Returns:
        league (str): The league for the given sport
    """
    if sport == Sport.FOOTBALL:
        league = 'NFL'
    elif sport == Sport.HOCKEY:
        league = 'NHL'
    elif sport == Sport.BASKETBALL:
        league = 'NBA'
    elif sport == Sport.WOMENS_BASKETBALL:
        league = 'WNBA'
    elif sport == Sport.CRICKET:
        league = 'ICC'
    elif sport == Sport.ULTIMATE:
        league = 'USAU'
    else:
        league = 'Unknown'
    
    # Return lowercase if requested    
    if lower:
        league = league.lower()
    return league