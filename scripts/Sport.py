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
    if sport.value == Sport.FOOTBALL.value:
        league = 'NFL'
    elif sport.value == Sport.HOCKEY.value:
        league = 'NHL'
    elif sport.value == Sport.BASKETBALL.value:
        league = 'NBA'
    elif sport.value == Sport.WOMENS_BASKETBALL.value:
        league = 'WNBA'
    elif sport.value == Sport.CRICKET.value:
        league = 'ICC'
    elif sport.value == Sport.ULTIMATE.value:
        league = 'USAU'
    else:
        league = 'UNKNOWN'
    
    # Return lowercase if requested    
    if lower:
        league = league.lower()
    return league

def get_sport_from_str(string: str):
    """Gets the sport from the given string

    Args:
        string (str): The string to get the sport from

    Returns:
        sport (Sport): The sport for the given string
    """
    if string == 'Football':
        sport = Sport.FOOTBALL
    elif string == 'Hockey':
        sport = Sport.HOCKEY
    elif string == 'Basketball':
        sport = Sport.BASKETBALL
    elif string == 'Womens Basketball':
        sport = Sport.WOMENS_BASKETBALL
    elif string == 'Cricket':
        sport = Sport.CRICKET
    elif string == 'Ultimate':
        sport = Sport.ULTIMATE
    else:
        sport = None
    return sport


if __name__ == "__main__":
    print(get_league(Sport.FOOTBALL))