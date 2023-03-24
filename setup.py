#################################################################
# Filename: setup.py                                            #
# Author: Bryce Whitney                                         #
# Last Edit: 3/24/2023                                          #
#                                                               #
# Description: Performs all the necessary setup for the project #
#################################################################

# Imports
import os
import nltk
from scripts.constants import TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH
# Install the necessary libraries
print("Installing the necessary libraries...")
os.system("pip install -r requirements.txt")

# Download the necessary nltk packages
print("Downloading nltk punkt and stopwords packages...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load the text data if the foler is empty
if len(os.listdir(TEXT_DATA_FOLDER_PATH)) == 0:
    print("Loading the text data...")
    os.system("python scripts/generate_data.py")
    
# Process the data if necessary
if len(os.listdir(PROCESSED_DATA_FOLDER_PATH)) == 0:
    print("Processing the data...")
    os.system("python scripts/text_preprocessing.py")
    