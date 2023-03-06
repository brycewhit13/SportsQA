####################################################################
# Filename: text_preprocessing.py                                  #
# Author: Bryce Whitney                                            #
# Last Edit: 3/6/2023                                              #
#                                                                  #
# Description: This script performs text preprocessing on the data #
# and stores the results in the processed_data folder that can be  #
# used in the model.                                               #
####################################################################

# Imports
import os
import string
import nltk
from nltk.corpus import stopwords
from constants import TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH, STOPWORDS_SET

#############
# Functions #
#############
def process_text(data_file, output_file, remove_stopwords=False, remove_punctuation=False):
    """Processes the text data from the text_data folder and stores the results in the processed_data folder.

    Args:
        data_file (str): The file name of the data to process
        output_file (str): The file name to store the processed data
    """
    # Read in the data
    data = load_text_data(data_file)
    
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
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data_processed)
        
    def load_text_data(data_file):
        """Loads the text data from the given data txt file

        Args:
            data_file (str): The file name of the data to load

        Returns:
            str: The processed text data
        """
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
        str: The data with stopwords removed
    """
    # Remove stopwords
    data_processed = " ".join([word for word in data.split() if word not in STOPWORDS_SET])
    return data_processed

def _remove_punctuation(data):
    """Removes punctuation from the data

    Args:
        data (str): The data to remove punctuation from

    Returns:
        str: The data with punctuation removed
    """
    data_processed = " ".join([word for word in data.split() if word not in string.punctuation])
    return data_processed
        
#################
# Main function #
#################
if __name__ == "__main__":
    # Process NFL Rules
    print("Processing NFL Rules...")
    nfl_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "nfl_rules.txt")
    nfl_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "nfl_rules_processed.txt")
    process_text(nfl_text_file, nfl_output_file)
    
    # Process NHL Rules
    print("Processing NHL Rules...")
    nhl_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "nhl_rules.txt")
    nhl_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "nhl_rules_processed.txt")
    process_text(nhl_text_file, nhl_output_file)
    
    # Process NBA Rules
    print("Processing NBA Rules...")
    nba_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "nba_rules.txt")
    nba_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "nba_rules_processed.txt")
    process_text(nba_text_file, nba_output_file)
    
    # Process WNBA Rules
    print("Processing WNBA Rules...")
    wnba_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "wnba_rules.txt")
    wnba_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "wnba_rules_processed.txt")
    process_text(wnba_text_file, wnba_output_file)
    
    # Process Cricket Rules
    print("Processing Cricket Rules...")
    cricket_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "cricket_rules.txt")
    cricket_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "cricket_rules_processed.txt")
    process_text(cricket_text_file, cricket_output_file)
    
    # Process ultimate Rules
    print("Processing Ultimate Rules...")
    ultimate_text_file = os.path.join(TEXT_DATA_FOLDER_PATH, "ultimate_rules.txt")
    ultimate_output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, "ultimate_rules_processed.txt")
    process_text(ultimate_text_file, ultimate_output_file)