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
from text_preprocessing import load_text_data
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers


##### FUNCTIONS #####
def get_user_question():
    question = input("Please enter a question: ")
    return question

def get_answer(question, file_path):
    # Initialize the retriever and reader
    document_store = InMemoryDocumentStore(use_bm25=True)
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)
    
    # Convert the text into document objects
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run(file_path=file_path)
    
    # Initialize the pipeline and retrieve an answer
    pipe = ExtractiveQAPipeline(reader, retriever)
    answer = pipe.run(query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}})
    
    return answer

##### MAIN #####
if __name__ == "__main__":    
    context_path = os.path.join(PROCESSED_DATA_FOLDER_PATH, "ultimate_sample.txt")
    
    question = "How many players are on the field for each team?"
    answer = get_answer(question, context_path)
    
    question2 = "What is the event organizer clause?"
    answer2 = get_answer(question2, context_path)
    
    print_answers(answer, details="minimum")
    print_answers(answer2, details="minimum")