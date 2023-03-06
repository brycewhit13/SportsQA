####################################################################
# Filename: extractive_summarization.py                            #
# Author: Bryce Whitney                                            #
# Last Edit: 3/6/2023                                              #
#                                                                  #
# Description: This script performs extractive summarization       #
# for the rulebooks of the different sports with the TextRank      #
# method                                                           #
####################################################################


# TODO:
# - Implement for each individual sport, not just a sample
# - Remove sample_ultimate.txt from processed_data folder
# - Compare the results to the abstractive summarization results

# Imports
import os
from nltk import sent_tokenize
from constants import PROCESSED_DATA_FOLDER_PATH
from text_preprocessing import load_text_data, _remove_stopwords

#############
# FUNCTIONS #
#############

def extractive_summarization():
    """Performs extractive summarization on the rulebooks using the TextRank method
    """
    # Read in the data
    data = load_text_data(os.path.join(PROCESSED_DATA_FOLDER_PATH, "sample_ultimate.txt"))
    
    # Process the data
    data_processed = _remove_stopwords(data)
    sentences = sent_tokenize(data_processed)
    
    # Vectorize the features
    # Generate the adjacency matrix
    # Summarize the text
    # Return the summarization
    
    
def tfidf_vectorize():
    """Calculates the tfidf vector for each sentence
    """
    raise NotImplementedError()
    
def word_count_vectorize():
    """Calculates the word count vector for each sentence
    """
    raise NotImplementedError()

def generate_similarity_matrix():
    """Generates the similarity matrix for the sentences
    """
    raise NotImplementedError()
    
#################
# MAIN FUNCTION #
#################

if __name__ == "__main__":
    raise NotImplementedError()