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

# Imports 
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from text_preprocessing import load_text_data
from constants import PROCESSED_DATA_FOLDER_PATH

#############
# FUNCTIONS #
#############

def generative_summary(text_data, min_summary_length=10, max_summary_length=200):
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
    summary = chunked_summary(input_text=text_data, model=model, tokenizer=tokenizer, min_chunk_len=10, max_chunk_len=200)
    
    print(f'Length of the source document: {len(text_data)}')
    print(f'Length of the summary: {len(summary)}')
    
    return summary
    
def truncate_summary(input_text, model, tokenizer, min_length, max_length):
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


def chunked_summary(input_text, model, tokenizer, min_chunk_len, max_chunk_len):
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
    for chunk in chunked_inputs:
        chunk = ''.join(chunk)
        chunk_summary = truncate_summary(input_text=chunk, model=model, tokenizer=tokenizer, min_length=min_chunk_len, max_length=max_chunk_len)
        chunk_summary = chunk_summary.split('</s>')[-2].split('<s>')[-1].strip()
        summary += (' '+chunk_summary)
    return summary

    

#################
# MAIN FUNCTION #
#################

if __name__ == "__main__":
    data = load_text_data(os.path.join(PROCESSED_DATA_FOLDER_PATH, "ultimate_sample.txt"))
    summary = generative_summary(text_data=data)
    print(summary)