############################################################################################################
# Filename: summarization.py                                                                               #
# Author: Bryce Whitney                                                                                    #
# Last Edit: 4/24/2023                                                                                     #
#                                                                                                          #
# Description: This script contains methods for abstractive and extractive summarizations                  #                                                                            #
#                                                                                                          #
# References: https://github.com/AIPI540/AIPI540-Deep-Learning-Applications/blob/main/3_nlp/summarization/ #
############################################################################################################

##### Imports #####
import numpy as np
import networkx as nx
from nltk import sent_tokenize
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from data_processing import load_processed_data
from constants import STOPWORDS_SET

####################################
##### Extractive Summarization #####
####################################
def extractive_summarization(datafile: str, top_n: int = 5):
    """Performs extractive summarization on the rulebooks using the TextRank method
    
    Args:
        datafile (str): The path to the datafile
        top_n (int): The number of sentences to include in the summary. Defaults to 5.
    """
    # Read in the data
    print("loading data...")
    data = load_processed_data(datafile)
    
    # Remove stopwords
    print("processing data...")
    data_no_stopwords = " ".join([word for word in data.split() if word not in STOPWORDS_SET])
    
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
    
    
def tfidf_vectorize(sentences: list):
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
    
def word_count_vectorize(sentences: list):
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

def generate_similarity_matrix(feature_vecs: list):
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
    
def pagerank_summarization(sentences: list, similarity_matrix, top_n: int = 5):
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

#####################################
##### Abstractive Summarization #####
#####################################

def generative_summary(text_data: str, min_summary_length: int = 10, max_summary_length: int = 200):
    """Generates a summary of the input text using the HuggingFace model sshleifer/distilbart-cnn-12-6

    Args:
        text_data (str): data to be summarized
        min_summary_length (int, optional): the min length of the resulting summary. Defaults to 10.
        max_summary_length (int, optional): the max length of the resulting summary. Defaults to 200.

    Returns:
        _type_: _description_
    """
    # Instatiate the model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    
    # Generate and return the summary
    summary = chunked_summary(input_text=text_data, model=model, tokenizer=tokenizer, min_chunk_len=min_summary_length, max_chunk_len=max_summary_length)
    
    # Return the summary
    return summary
    
def truncate_summary(input_text: str, model: AutoModelForSeq2SeqLM, tokenizer: AutoTokenizer, min_length: int, max_length: int):
    """Truncates the summary to the desired length

    Args:
        input_text (str): _description_
        model (AutoModelForSeq2SeqLM): model that will generate the summary
        tokenizer (AutoTokenizer): tokenizer for the model
        min_length (int): min length of the summary
        max_length (int): max length of the summary

    Returns:
        str: a truncated version of the input summary
    """
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, length_penalty=1.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0])

def chunked_summary(input_text: str, model: AutoModelForSeq2SeqLM, tokenizer: AutoTokenizer, min_chunk_len: int, max_chunk_len: int):
    """Split the input text into chunks of 1024 and generate a summary for each chunk.
    These chunks are then concatenated to form the final summary.

    Args:
        input_text (str): the input text to be summarized
        model (AutoModelForSeq2SeqLM): model for generating the summary
        tokenizer (AutoTokenizer): tokenizer for the model
        min_chunk_len (int): min length of each chunk
        max_chunk_len (int): max length of each chunk

    Returns:
        str: A summary of the input text
    """
    # Separate the input text into chunks
    input_text = input_text.split(' ')
    chunked_inputs = [input_text[i:i+1024] for i in range(0,len(input_text),1024)]
    summary = ''
    
    # Get input for each chunk
    for i, chunk in enumerate(chunked_inputs):
        chunk = ' '.join(chunk)
        chunk_summary = truncate_summary(input_text=chunk, model=model, tokenizer=tokenizer, min_length=min_chunk_len, max_length=max_chunk_len)
        chunk_summary = chunk_summary.split('</s>')[-2].split('<s>')[-1].strip()
        
        # Add space between chunks if not the first chunk
        if(i == 0):
            summary += chunk_summary
        else:
            summary += (' '+chunk_summary)
            
    # Return the summary        
    return summary