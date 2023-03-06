##########################################################################
# Filename: constants.py                                                 #
# Author: Bryce Whitney                                                  #
# Last Edit: 3/6/2023                                                    #
#                                                                        #
# Description: A file containing constants needed throughout the project #
##########################################################################
# Imports
import nltk
from nltk.corpus import stopwords

# CONSTANTS
RAW_DATA_FOLDER_PATH = "../data/raw_data"
TEXT_DATA_FOLDER_PATH = "../data/text_data"
PROCESSED_DATA_FOLDER_PATH = "../data/processed_data"

try:
    STOPWORDS_SET = set(stopwords.words("english"))
except:
    nltk.download('stopwords', quiet=True)
    STOPWORDS_SET = set(stopwords.words("english"))