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

from scripts.constants import TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH, RAW_DATA_FOLDER_PATH
from scripts.data_processing import establish_connection, download_all_data
# Install the necessary libraries
print("Installing the necessary libraries...")
os.system("pip install -r requirements.txt")

# Download the necessary nltk packages
print("Downloading nltk punkt and stopwords packages...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Ensure all the data folders exist
if not os.path.exists(RAW_DATA_FOLDER_PATH):
    os.mkdir(RAW_DATA_FOLDER_PATH)
if not os.path.exists(TEXT_DATA_FOLDER_PATH):
    os.mkdir(TEXT_DATA_FOLDER_PATH)
if not os.path.exists(PROCESSED_DATA_FOLDER_PATH):
    os.mkdir(PROCESSED_DATA_FOLDER_PATH)

# Download the data from azure
print("Downloading the data from azure...")
blob_service_client, container_client = establish_connection()
download_all_data(container_client)
    