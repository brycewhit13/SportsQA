##########################################################################
# Filename: constants.py                                                 #
# Author: Bryce Whitney                                                  #
# Last Edit: 3/24/2023                                                   #
#                                                                        #
# Description: A file containing constants needed throughout the project #
##########################################################################

# Imports
import os
from nltk.corpus import stopwords

# CONSTANTS
RAW_DATA_FOLDER_PATH = os.path.join("data", "raw_data")
TEXT_DATA_FOLDER_PATH = os.path.join("data", "text_data")
PROCESSED_DATA_FOLDER_PATH = os.path.join("data", "processed_data")
STOPWORDS_SET = set(stopwords.words("english"))