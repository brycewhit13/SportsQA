#################################################################
# Filename: setup.py                                            #
# Author: Bryce Whitney                                         #
# Last Edit: 4/4/2023                                           #
#                                                               #
# Description: Performs all the necessary setup for the project #
#################################################################

# Imports
import os
import nltk
import sys
sys.path.append('scripts')

from scripts.constants import TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH, RAW_DATA_FOLDER_PATH, DOCUMENT_STORE_FOLDER_PATH

# Install the necessary libraries
print("Installing the necessary libraries...")
os.system("pip install -r requirements.txt")

# Download the necessary nltk packages
print("Downloading nltk punkt and stopwords packages...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
    
print("Setup complete!")