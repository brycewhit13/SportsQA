##########################################################################
# Filename: constants.py                                                 #
# Author: Bryce Whitney                                                  #
# Last Edit: 4/24/2023                                                   #
#                                                                        #
# Description: A file containing constants needed throughout the project #
##########################################################################

# Imports
import os
from nltk.corpus import stopwords

##### CONSTANTS #####
# Path Constants
RAW_DATA_FOLDER_PATH = os.path.join("data", "raw_data")
TEXT_DATA_FOLDER_PATH = os.path.join("data", "text_data")
PROCESSED_DATA_FOLDER_PATH = os.path.join("data", "processed_data")
DOCUMENT_STORE_FOLDER_PATH = os.path.join("data", "document_store")
SUMMARY_FOLDER_PATH = os.path.join("data", "summary")
FINAL_SUMMARIES_FOLDER_PATH = os.path.join("data", "final_summaries")

# Modeling Constants
STOPWORDS_SET = set(stopwords.words("english"))