####################################################################
# Filename: text_preprocessing.py                                  #
# Author: Bryce Whitney                                            #
# Last Edit: 3/24/2023                                             #
#                                                                  #
# Description: This script performs text preprocessing on the data #
# and stores the results in the processed_data folder that can be  #
# used in the model.                                               #
####################################################################

# Imports
import os
import string
from constants import TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH, STOPWORDS_SET
from Sport import Sport, get_league

#############
# Functions #
#############
def process_text(sport: Sport, remove_stopwords: bool = False, remove_punctuation: bool = False):
    """Processes the text data from the text_data folder and stores the results in the processed_data folder.

    Args:
        data_file (str): The file name of the data to process
        output_file (str): The file name to store the processed data
    """
    # Read in the data
    data_file = os.path.join(TEXT_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules.txt")
    data = _load_text_data(data_file)
    
    # Make everything lowercase
    data_processed = data.lower()
    # Replace non alphanumeric characters with empty strings
    data_processed = data_processed.replace("[^a-zA-Z0-9_]", "")
    # Remove Stopwords and Punctuation if necessary
    if(remove_stopwords == True):
        data_processed = _remove_stopwords(data_processed)
    if(remove_punctuation == True):
        data_processed = _remove_punctuation(data_processed)
    if(remove_stopwords == False and remove_punctuation == False):
        data_processed = " ".join([word for word in data_processed.split()])
    
    # Save the processed data to the output file
    output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data_processed)    
    
    
def load_processed_data(sport: Sport):
    """Loads the processed data from the processed_data folder

    Args:
        sport (Sport): The sport to load the data for

    Returns:
        str: The processed text data
    """
    data_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

####################
# Helper Functions #
####################
def _remove_stopwords(data):
    """Removes stopwords from the data

    Args:
        data (str): The data to remove stopwords from

    Returns:
        data_processed (str): The data with stopwords removed
    """
    # Remove stopwords
    data_processed = " ".join([word for word in data.split() if word not in STOPWORDS_SET])
    return data_processed

def _remove_punctuation(data):
    """Removes punctuation from the data

    Args:
        data (str): The data to remove punctuation from

    Returns:
        data_processed (str): The data with punctuation removed
    """
    data_processed = " ".join([word for word in data.split() if word not in string.punctuation])
    return data_processed

def _load_text_data(data_file: str):
    """Loads the text data from the given data txt file

    Args:
        data_file (str): The file name of the data to load

    Returns:
        data (str): The processed text data as a string
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data
        
#################
# Main function #
#################
if __name__ == "__main__":
    for sport in Sport:
        print(f"Processing {sport.value} Rules...")
        process_text(sport)