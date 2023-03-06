##########################################################################################################################################
# Filename: abstractive_sumarization.py                                                                                                  #
# Author: Bryce Whitney                                                                                                                  #
# Last Edit: 3/6/2023                                                                                                                    #
#                                                                                                                                        #
# Description: This script performs abstractive summarization                                                                            #
# for the rulebooks of the different sports                                                                                              #
#                                                                                                                                        #
# References: https://github.com/AIPI540/AIPI540-Deep-Learning-Applications/blob/main/3_nlp/summarization/generative_summarization.ipynb #
##########################################################################################################################################


# TODO:
# - Try different models
# - Implement for each individual sport, not just a sample
# - Remove ultimate_sample.txt from processed_data folder
# - Compare the results to the abstractive summarization results

# Imports 
import os
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from text_preprocessing import load_text_data
from constants import PROCESSED_DATA_FOLDER_PATH

#############
# FUNCTIONS #
#############

def generative_summary(datafile, min_summary_length=10, max_summary_length=100):
    # Load the data
    data = load_text_data(datafile)
    
    # Instatiate the model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    
    # Generate and return the summary
    summary = chunked_summary(input_text=data, model=model, tokenizer=tokenizer, min_chunk_len=30, max_chunk_len=100)
    
    print(f'Length of the source document: {len(data)}')
    print(f'Length of the summary: {len(summary)}')
    
    return summary
    
def truncate_summary(input_text, model, tokenizer, min_length, max_length):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, length_penalty=1.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0])


def chunked_summary(input_text, model, tokenizer, min_chunk_len, max_chunk_len):
    # Separate the input text into chunks
    input_text = input_text.split(' ')
    chunked_inputs = [input_text[i:i+1024] for i in range(0,len(input_text),1024)]
    summary = ''
    
    # Get input for each chunk
    for chunk in chunked_inputs:
        chunk = ' '.join(chunk)
        chunk_summary = truncate_summary(input_text=chunk, model=model, tokenizer=tokenizer, min_length=min_chunk_len, max_length=max_chunk_len)
        chunk_summary = chunk_summary.split('')[-2].split('<s>')[-1].strip()
        summary += (' '+chunk_summary)
    return summary

    

#################
# MAIN FUNCTION #
#################

if __name__ == "__main__":
    summary = generative_summary(os.path.join(PROCESSED_DATA_FOLDER_PATH, "ultimate_sample.txt"))
    print(summary)