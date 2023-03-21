##########################################################################################################################################
# Filename: extractive_summarization.py                                                                                                  #
# Author: Bryce Whitney                                                                                                                  #
# Last Edit: 3/21/2023                                                                                                                   #
#                                                                                                                                        #
# Description: This script performs extractive summarization                                                                             #
# for the rulebooks of the different sports with the TextRank                                                                            #
# method                                                                                                                                 #
#                                                                                                                                        #
# References: https://github.com/AIPI540/AIPI540-Deep-Learning-Applications/blob/main/3_nlp/summarization/extractive_summarization.ipynb #
##########################################################################################################################################

# Imports
import os
import numpy as np
import networkx as nx
from nltk import sent_tokenize
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from constants import PROCESSED_DATA_FOLDER_PATH
from text_preprocessing import load_text_data, _remove_stopwords

#############
# FUNCTIONS #
#############

def extractive_summarization(datafile, top_n=5):
    """Performs extractive summarization on the rulebooks using the TextRank method
    """
    # Read in the data
    print("loading data...")
    data = load_text_data(datafile)
    
    # Remove stopwords
    print("processing data...")
    data_no_stopwords = _remove_stopwords(data)
    
    # Extract sentences
    sentences_extracted = sent_tokenize(data)
    sentences_processed = sent_tokenize(data_no_stopwords)
    
    # Vectorize the features
    print("vectorizing features...")
    #feature_vecs = word_count_vectorize(sentences_processed)
    feature_vecs = tfidf_vectorize(sentences_processed)
    
    # Generate the adjacency matrix
    print("generating adjacency matrix...")
    adjacency_matrix = generate_similarity_matrix(feature_vecs)
    
    # Summarize the text
    print("summarizing text...")
    summary = pagerank_summarization(sentences_extracted, adjacency_matrix, top_n=top_n)
    
    # Return the summarization
    return summary
    
    
def tfidf_vectorize(sentences):
    """Calculates the tfidf vector for each sentence
    
    Args:
        sentences (list): A list of sentences
    
    Returns: 
        feature_vecs (list): A list of feature vectors
    """
    # Create features with TfidfVectorizer
    vectorizer = TfidfVectorizer()
    feature_vecs = vectorizer.fit_transform(sentences)
    feature_vecs = feature_vecs.todense().tolist()
    
    # Return the features
    return feature_vecs
    
def word_count_vectorize(sentences):
    """Calculates the word count vector for each sentence
    
    Args:
        sentences (list): A list of sentences
    
    Returns:
        feature_vecs (list): A list of feature vectors
    """
    # Get vocabulary for entire document
    sentences = [sent.split(' ') for sent in sentences]
    all_words = list(set([word for s in sentences for word in s]))

    # Create feature vector for each sentence
    feature_vecs = []
    for sentence in sentences:
        feature_vec = [0] * len(all_words)
        for word in sentence:
            feature_vec[all_words.index(word)] += 1
        feature_vecs.append(feature_vec)
    
    # Return the feature vectors
    return feature_vecs

def generate_similarity_matrix(feature_vecs):
    """Generates the similarity matrix for the sentences
    
    Args:
        feature_vecs (list): A list of feature vectors
        
    Returns:
        similarity_matrix (np.array): A numpy array of the similarity matrix between features
    """
    # Create empty adjacency matrix
    similarity_matrix = np.zeros((len(feature_vecs), len(feature_vecs)))
 
    # Populate the adjacency matrix using the similarity of all pairs of sentences
    for i in range(len(feature_vecs)):
        for j in range(len(feature_vecs)):
            if i == j: #ignore if both are the same sentence
                continue 
            similarity_matrix[i][j] = 1 - cosine_distance(feature_vecs[1], feature_vecs[j])
    
    # Return the similarity matrix
    return similarity_matrix
    
def pagerank_summarization(sentences, similarity_matrix, top_n=5):
    """Applies the PageRank algorithm to the similarity matrix to get the most important sentences
    from the corpus to generate a representative summary

    Args:
        sentences (list): a list of the sentences
        similarity_matrix (np.ndarray): a numpy array of the similarity matrix between features
        top_n (int, optional): The number of sentences to use as the summarization. Defaults to 5.

    Returns:
        summary (str): A string of the extracted sentences making up the summary
    """
    # Create the graph representing the document
    document_graph = nx.from_numpy_array(similarity_matrix)

    # Apply PageRank algorithm to get centrality scores for each node/sentence
    scores = nx.pagerank(document_graph)
    scores_list = list(scores.values())

    # Sort and pick top sentences
    ranking_idx = np.argsort(scores_list)[::-1]
    ranked_sentences = [sentences[i] for i in ranking_idx]   

    summary = []
    for i in range(top_n):
        summary.append(ranked_sentences[i])

    summary = " ".join(summary)

    return summary

#################
# MAIN FUNCTION #
#################

if __name__ == "__main__":
    summary = extractive_summarization(datafile=os.path.join(PROCESSED_DATA_FOLDER_PATH, "ultimate_sample.txt"), top_n=3)
    print(summary)