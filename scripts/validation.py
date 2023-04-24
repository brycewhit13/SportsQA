#########################################################################
# Filename: validation.py                                               #
# Author: Bryce Whitney                                                 #
# Last Edit: 4/24/2023                                                  #
#                                                                       #
# Description: Script to perform validation on the different approaches #                                                                                                                                #
#########################################################################

##### Imports #####
import os
import pandas as pd

from Sport import get_sport_from_str
from question_answering import get_tfidf_answer, query_document_store, gpt_answer_no_context, gpt_answer_with_context

if __name__ == "__main__":
    # Load the validation questions
    validation_folder = os.path.join("..", "validation")
    validation_set = pd.read_csv(os.path.join(validation_folder, "test_questions.csv"), )

    # Get a list of all the questions
    question_list = validation_set["Question"].tolist()
    sports_list = validation_set["Sport"].tolist()
    
    # Store the answers for each method
    tfidf_answers = []
    extractive_pipeline_answers = []
    extractive_pipeline_context = []
    openai_gpt_answers = []
    gpt_answers_no_context = []
    
    # Loop through the questions and get the answers
    for i, (question, sport_name) in enumerate(zip(question_list, sports_list)):
        # Get the sport
        sport = get_sport_from_str(sport_name)
        
        # Get the answers
        tf_ans = get_tfidf_answer(question, sport, processed_data_folder_path=os.path.join("..","data", "processed_data"))
        tfidf_answers.append(tf_ans)
        
        doc_store_ans, doc_store_context = query_document_store(question, sport, document_folder_path=os.path.join("..","data", "document_store"))
        extractive_pipeline_answers.append(doc_store_ans)
        extractive_pipeline_context.append(doc_store_context)
        
        gpt_ans = gpt_answer_with_context(question, sport, summary_folder=os.path.join("..","data", "summary"))
        openai_gpt_answers.append(gpt_ans)
        
        gpt_ans_no_context = gpt_answer_no_context(question, sport, summary_folder=os.path.join("..","data", "summary"))
        gpt_answers_no_context.append(gpt_ans_no_context)
        
        if i % 10 == 0:
            print(f"Finished {i}/{len(question_list)} questions")
        
    # Save the results to csv files
    tfidf_df = pd.DataFrame({"Question":question_list, "Sport":sports_list, "Answer":tfidf_answers})
    tfidf_df.to_csv(os.path.join(validation_folder, "tfidf_answers.csv"))
    
    extract_df = pd.DataFrame({"Question":question_list, "Sport":sports_list, "Answer":extractive_pipeline_answers, "Context":extractive_pipeline_context})
    extract_df.to_csv(os.path.join(validation_folder, "extractive_pipeline_answers.csv"))
    
    gpt_context_df = pd.DataFrame({"Question":question_list, "Sport":sports_list, "Answer":openai_gpt_answers})
    gpt_context_df.to_csv(os.path.join(validation_folder, "gpt_answers_with_context.csv"))   
    
    gpt_no_context_df = pd.DataFrame({"Question":question_list, "Sport":sports_list, "Answer":gpt_answers_no_context})
    gpt_no_context_df.to_csv(os.path.join(validation_folder, "gpt_answers_no_context.csv")) 