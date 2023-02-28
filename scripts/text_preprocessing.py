####################################################################
# Filename: text_preprocessing.py                                  #
# Author: Bryce Whitney                                            #
# Last Edit: 2/27/2023                                             #
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

# Constants
TEXT_DATA_FOLDER_PATH = "../data/text_data"
PROCESSED_DATA_FOLDER_PATH = "../data/processed_data"

#############
# Functions #
#############
def process_text(data_file, output_file):
    """Processes the text data from the text_data folder and stores the results in the processed_data folder.

    Args:
        data_file (str): The file name of the data to process
        output_file (str): The file name to store the processed data
    """
    # Read in the data
    data = _read_text_data(data_file)
    
    # Make everything lowercase
    data_processed = data.lower()
    # Replace non alphanumeric characters with empty strings
    data_processed = data_processed.replace("[^a-zA-Z0-9_]", "")
    # Remove Stopwords and Punctuation
    try:
        stopwords_set = set(stopwords.words("english"))
    except:
        nltk.download('stopwords')
        stopwords_set = set(stopwords.words("english"))
    
    data_processed = " ".join([word for word in data_processed.split() if word not in stopwords_set and word not in string.punctuation])
    
    # Save the processed data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data_processed)

####################
# Helper Functions #
####################
def _read_text_data(data_file):
    """Reads the text data from the text_data folder

    Args:
        data_file (str): The file name of the data to read

    Returns:
        str: The text data
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data
        
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