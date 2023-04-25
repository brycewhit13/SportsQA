##########################################################################################################################################
# Filename: question_answering.py                                                                                                        #
# Author: Bryce Whitney                                                                                                                  #
# Last Edit: 4/24/2023                                                                                                                   #
#                                                                                                                                        #
# Description: This script performs question and answering                                                                               #
# for the rulebooks of the different sports with HuggingFace models                                                                      #                                                                                                                                #
#                                                                                                                                        #
# References: https://github.com/AIPI540/AIPI540-Deep-Learning-Applications/blob/main/3_nlp/summarization/extractive_summarization.ipynb #
##########################################################################################################################################

##### Imports #####
import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from haystack.nodes import FARMReader, DensePassageRetriever
from haystack.pipelines import ExtractiveQAPipeline

from constants import PROCESSED_DATA_FOLDER_PATH, DOCUMENT_STORE_FOLDER_PATH, FINAL_SUMMARIES_FOLDER_PATH
from Sport import Sport, get_league
from data_processing import get_document_store, load_processed_data, load_summary_data

#####################
##### FUNCTIONS #####
#####################
def query_document_store(question: str, sport: Sport, document_folder_path: str = DOCUMENT_STORE_FOLDER_PATH):
    """Queries the document store to try and answer the user's question

    Args:
        question (str): The question the user asked
        sport (Sport): The sport the user selected
        document_folder_path (str, optional): The folder containing the document store databases. Defaults to DOCUMENT_STORE_FOLDER_PATH.

    Returns:
        tuple: The answer to the questions and the context from where the answer was pulled
    """
    # Get the appropriate document store
    document_store = get_document_store(sport, document_folder_path=document_folder_path)
    
    # intialize DensePassageRetriever and reader
    retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
    )
    reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)

    # Initialize the pipeline and retrieve an answer
    pipe = ExtractiveQAPipeline(reader, retriever)
    answer_obj = pipe.run(query=question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
    
    # Extract the answer and context from the answer object
    answer = answer_obj["answers"][0].answer
    context = answer_obj["answers"][0].context
    
    # Return the answer and the context
    return answer, context

def gpt_answer_no_context(question: str, sport: Sport):
    """Attemps to answer the question using GPT-3.5 without giving it any context

    Args:
        question (str): The question the user asked
        sport (Sport): The sport the user selected

    Returns:
        str: The answer to the question
    """
    # Get the appropriate sport league
    sport_league = get_league(sport)
    
    # Establish the prompt for the GPT-3.5 model
    prompt = f"Following the most recent {sport_league} rules, answer the following question. \n\nQuestion: {question}"

    # Make a request to GPT-3.5
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                            messages=[{
                                                "role":"user", 
                                                "content":prompt
                                                }],
                                            temperature=0.1,
                                            )
    
    answer = response['choices'][0]['message']['content']
    answer = answer.replace("Answer: ", "").strip()
    return answer

def gpt_answer_with_context(question: str, sport: Sport, summary_folder: str = FINAL_SUMMARIES_FOLDER_PATH):
    """Attempts to answer the question using GPT-3.5 while providing it a summary of the rules 
    when the model is not confident in the answer. If it is still not confident with the added context,
    the user will be informed in the answer. 

    Args:
        question (str): The question the user asked
        sport (Sport): The sport the user selected
        summary_folder (str, optional): Path to the folder containing the summaries for each sport. Defaults to FINAL_SUMMARIES_FOLDER_PATH.

    Returns:
        str: The answer to the question
    """
    # Get the appropriate sport league and data
    sport_league = get_league(sport)
    
    # Get the gpt answer
    gpt_answer = gpt_answer_no_context(question, sport)
    
    # If the model doesn't know the answer, use the summary
    if "as an ai language model" in gpt_answer.lower():
        summary = ""
        with open(os.path.join(summary_folder, sport_league + "_summary_final.txt"), "r") as file:
            summary = file.read()
        
        prompt = f"Following the most recent {sport_league} rules, answer the following question. \n\nQuestion: {question}"
        
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[
                                                {
                                                    "role":"user",
                                                    "content":prompt
                                                },
                                                {
                                                    "role":"assistant",
                                                    "content":f"Here is a brief summary of the rules: {summary}"
                                                }
                                                ],
                                                temperature=0.1,
        )
        
        context_answer = response['choices'][0]['message']['content']
    
        if "as an ai language model" in context_answer.lower() or "i'm sorry" in context_answer.lower() or "i apologize" in context_answer.lower() or "summary provided" in context_answer.lower():
            # This means neither answer is confident
            # Remove the first sentence from the answer and tell the user we are not confident before returning
            answer = gpt_answer[gpt_answer.find(".")+1:]
            answer = "I am not entirely confident in my answer, so I recommend you explore the official rulebook for the answer to your question." + answer
            return answer
        else:
            return context_answer.replace("Answer: ", "").strip()
    else:
        return gpt_answer

def get_tfidf_answer(question: str, sport: Sport, processed_data_folder_path: str = PROCESSED_DATA_FOLDER_PATH):
    """Uses TF-IDF to find the sentence with the highest cosine similarity to the question and returns that sentence as the answer

    Args:
        question (str): The question to be answered
        sport (Sport): The sport of the rulebook
        processed_data_folder_path (str, optional): The path to the processed data folder. Defaults to PROCESSED_DATA_FOLDER_PATH.

    Returns:
        str: The answer which is the sentence with the highest cosine similarity to the question
    """
    # Load the processed data and get all the sentences
    data = load_processed_data(sport, folder_path=processed_data_folder_path)
    sentences = data.split(".")

    # Fit a TF-IDF vectorizer on the data
    vectorizer = TfidfVectorizer()
    sentence_embeddings = vectorizer.fit_transform(sentences)
    question_embedding = vectorizer.transform([question])
    
    # Calculate the cosine similarity between the question and each sentence
    cosine_similarities = cosine_similarity(question_embedding, sentence_embeddings)
    
    # Find the sentence with the highest cosine similarity
    answer = sentences[cosine_similarities.argmax()]
    return answer