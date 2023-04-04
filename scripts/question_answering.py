##########################################################################################################################################
# Filename: question_answering.py                                                                                                        #
# Author: Bryce Whitney                                                                                                                  #
# Last Edit: 3/21/2023                                                                                                                   #
#                                                                                                                                        #
# Description: This script performs question and answering                                                                               #
# for the rulebooks of the different sports with HuggingFace models                                                                      #                                                                                                                                #
#                                                                                                                                        #
# References: https://github.com/AIPI540/AIPI540-Deep-Learning-Applications/blob/main/3_nlp/summarization/extractive_summarization.ipynb #
##########################################################################################################################################

# Imports
import os
from constants import PROCESSED_DATA_FOLDER_PATH
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.pipelines import ExtractiveQAPipeline
from Sport import Sport, get_league

# TODO: Potential problem with newlines in the text file
# TODO: Maybe remove the article numbers in the preprocessing step

##### FUNCTIONS #####
def get_user_question():
    question = input("Please enter a question: ")
    return question

def get_answer(question: str, sport: Sport):
    # Get the file path
    league = get_league(sport)
    file_name = league + "_rules_processed.txt"
    file_path = os.path.join(PROCESSED_DATA_FOLDER_PATH, file_name)
    
    # Initialize the retriever and reader
    document_store = InMemoryDocumentStore(use_bm25=True)
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)
    
    # Convert the text into document objects
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run(file_path=file_path)

    # Initialize the pipeline and retrieve an answer
    pipe = ExtractiveQAPipeline(reader, retriever)
    answer_obj = pipe.run(query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}})
    
    # Extract the answer and context from the answer object
    answer = answer_obj["answers"][0].answer
    context = answer_obj["answers"][0].context
    
    # Return the answer and the context
    return answer, context

##### Testing #####
# TODO: DELETE ONCE UP AND RUNNING
# ! FOR TESTING PURPOSES ONLY
def _get_answer(question: str, file_path: str):
    # Initialize the retriever and reader
    document_store = InMemoryDocumentStore(use_bm25=True)
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)
    
    # Convert the text into document objects
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run(file_path=file_path)
    
    # Initialize the pipeline and retrieve an answer
    pipe = ExtractiveQAPipeline(reader, retriever)
    answer_obj = pipe.run(query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}})
    
    # Extract the answer and context from the answer object
    answer = answer_obj["answers"][0].answer
    context = answer_obj["answers"][0].context
    
    return answer, context


##### MAIN #####
if __name__ == "__main__":    
    context_path = "../data/processed_data/usau_sample_rules_processed.txt"
    
    question = "How many players are on the field for each team?"
    answer, context = _get_answer(question, context_path)
    
    question2 = "What is the event organizer clause?"
    answer2, context2 = _get_answer(question2, context_path)
    
    print("\n")
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Context: {context}")
    
    print("\n")
    print(f"Question: {question2}")
    print(f"Answer: {answer2}")
    print(f"Context: {context2}")
