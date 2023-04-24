####################################################################
# Filename: get_data.py                                            #
# Author: Bryce Whitney                                            #
# Last Edit: 4/24/2023                                             #
#                                                                  #
# Description: Contains functions for generating the data and      #
# uploading / downloading it from the Azure blob storage system.   #
####################################################################

# Imports
import os
import sys
import string
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from haystack.nodes import PreProcessor, DensePassageRetriever
from haystack.document_stores import FAISSDocumentStore
from haystack import Document

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from Sport import Sport, get_league
from constants import *

########################################
##### FAISS Document Store Methods #####
########################################
def get_document_store(sport: Sport, document_folder_path=DOCUMENT_STORE_FOLDER_PATH):
    """Get the FAISSDocumentStore object if it exists, otherwise create it

    Returns:
        FAISSDocumentStore: A FAISSDocumentStore object
    """
    # Get the league of the sport
    league = get_league(sport)
    
    # Path to the index file
    index_path=os.path.join(document_folder_path, league, f"{league}_index.faiss")
    config_path=os.path.join(document_folder_path, league, f"{league}_index.json")
    # If the index file exist, load the FAISSDocumentStore object
    print(f"Checking if {index_path} exists...")
    if os.path.exists(index_path):
        print("Loading FAISSDocumentStore object...")
        return FAISSDocumentStore.load(index_path=index_path, config_path=config_path)
    print("Doesn't exist, creating FAISSDocumentStore object...")
    return FAISSDocumentStore(sql_url=f"sqlite:///{document_folder_path}/{league}/faiss_document_store.db", faiss_index_factory_str="Flat")
   
#####################################
##### Data Generation Functions #####
#####################################
def pdf_to_text(filename: str, sport: Sport, start_page: int = 0, end_page: int = None, origin_folder: str = RAW_DATA_FOLDER_PATH, dest_folder: str = TEXT_DATA_FOLDER_PATH):
    """Loads text from a pdf file and saves it to a txt file. You can specify the start and end pages to load
    and the resulting text is stored in the text_data folder with the output_name as the file name.

    Args:
        filename (str): the filename in the raw data folder
        output_name (str): Output file name
        start_page (int, optional): the first page to load. Defaults to 0.
        end_page (int, optional): the last page to load. Defaults to None.
        origin_folder (str, optional): the folder to load the file from. Defaults to RAW_DATA_FOLDER_PATH.
        dest_folder (str, optional): the folder to save the file to. Defaults to TEXT_DATA_FOLDER_PATH.
    """
    # Load the rulebook from the PDF
    data = PdfReader(os.path.join(origin_folder, filename))
    
    # If no end page is specified, use the last page
    # Check to make sure it is valid if it is specified
    if(end_page is None):
        end_page = len(data.pages)
        
    if(end_page > len(data.pages)):
        end_page = len(data.pages)
        
    if(end_page < start_page):
        end_page = start_page
        
    # Extract the test from the rulebook
    text = ""
    for page in range(start_page, end_page):
        text += data.pages[page].extract_text()
    
    # Save to a txt file
    output_name = get_league(sport, lower=True) + '_rules.txt'
    with open(os.path.join(dest_folder, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

def scrape_ultimate_data(sport: Sport = Sport.ULTIMATE, dest_folder: str = TEXT_DATA_FOLDER_PATH):
    """Scrapes USAU ultimate rules from the website and saves to a txt file
    
    Args:
        sport (Sport, optional): The sport to scrape the rules for. Defaults to Sport.ULTIMATE.
        dest_folder (str, optional): the folder to save the file to. Defaults to TEXT_DATA_FOLDER_PATH.
    """
    # Store the url
    url = 'https://usaultimate.org/rules/'
    
    # Scrape the html from the webpage
    html = requests.get(url)
    
    # Parse the html
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all(name='li')[1:]
    
    # Extract the text from the results list
    text = ''
    for result in results:
        text += result.text
    
    # Save to a txt file
    output_name = get_league(sport, lower=True) + '_rules.txt'
    with open(os.path.join(dest_folder, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

########################################
##### Text Preprocessing Functions #####
########################################
def process_text(sport: Sport, remove_stopwords: bool = False, remove_punctuation: bool = False, origin_folder: str = TEXT_DATA_FOLDER_PATH, dest_folder: str = PROCESSED_DATA_FOLDER_PATH):
    """Processes the text data from the text_data folder and stores the results in the processed_data folder.

    Args:
        data_file (str): The file name of the data to process
        output_file (str): The file name to store the processed data
        origin_folder (str, optional): The folder to load the data from. Defaults to TEXT_DATA_FOLDER_PATH.
        dest_folder (str, optional): The folder to save the processed data to. Defaults to PROCESSED_DATA_FOLDER_PATH.
    """
    # Read in the data
    data = load_text_data(sport, folder_path=origin_folder)
    
    # Make everything lowercase
    data_processed = data.lower()
    # Replace non alphanumeric characters with empty strings
    data_processed = data_processed.replace("[^a-zA-Z0-9_]", "")
    # Remove Stopwords and Punctuation if necessary
    if(remove_stopwords == True):
        data_processed = " ".join([word for word in data.split() if word not in STOPWORDS_SET])
    if(remove_punctuation == True):
        data_processed = " ".join([word for word in data.split() if word not in string.punctuation])
    if(remove_stopwords == False and remove_punctuation == False):
        data_processed = " ".join([word for word in data_processed.split()])
    
    # Save the processed data to the output file
    output_file = os.path.join(dest_folder, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data_processed)
        

def chunk_processed_data(sport: Sport, split_length: int = 250, split_overlap: int = 100, processed_data_folder: str = PROCESSED_DATA_FOLDER_PATH, document_folder: str = DOCUMENT_STORE_FOLDER_PATH):
    """Chunks the data for the sport into multiple files and stores them in the document store for that sport

    Args:
        sport (Sport): The sport to chunk the data for
        split_length (int, optional): The length of each chunk. Defaults to 250.
        split_overlap (int, optional): The overlap between chunks. Defaults to 100.
        processed_data_folder (str, optional): The folder to load the processed data from. Defaults to PROCESSED_DATA_FOLDER_PATH.
        document_folder (str, optional): The folder to store the document store in. Defaults to DOCUMENT_STORE_FOLDER_PATH.
    """
    # Get the document store for the sport
    document_store = get_document_store(sport, document_folder_path=document_folder)
    league = get_league(sport, lower=True)
    
    # Delete any existing documents in the document store
    if(document_store.get_document_count() > 0):
        document_store.delete_documents()
    
    # Load the processed data
    text = load_processed_data(sport, folder_path=processed_data_folder)
    document = Document(content=text, content_type="text", meta={"name": league + "_rules"})
    
    # Chunk the data with the preprocessor
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by='word',
        split_length=split_length,
        split_overlap=split_overlap,
        split_respect_sentence_boundary=True,
        max_chars_check=sys.maxsize,
    )
    
    processed_docs = preprocessor.process([document])
    
    # Write the data to the document store
    document_store.write_documents(processed_docs)
    
    # intialize DensePassageRetriever
    retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
    )

    # update embeddings
    document_store.update_embeddings(retriever)
    
    # Save the document store and delete the databse
    document_store.save(index_path=os.path.join(document_folder, league, f"{league}_index.faiss"))
    
    
def summarize_rules(sport: Sport, min_length: int = 1000, max_length: int = 2250, processed_folder: str = PROCESSED_DATA_FOLDER_PATH, summary_folder: str = SUMMARY_FOLDER_PATH):
    """Summarizes the rules for the sport and saves the summary to the summary folder. 
    The length of the summary is between min_length and max_length

    Args:
        sport (Sport): The sport to summarize the rules for
        min_length (int, optional): The minimum length of the summary. Defaults to 1000.
        max_length (int, optional): The maximum length of the summary. Defaults to 2250.
        processed_folder (str, optional): Path to the processed data folder. Defaults to PROCESSED_DATA_FOLDER_PATH.
        summary_folder (str, optional): Path to the summary folder where the summaries will be saved. Defaults to SUMMARY_FOLDER_PATH.
    """
    # Load the processed data
    data = load_processed_data(sport, folder_path=processed_folder)
    
    # initialize model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

    # Separate the  text into chunks
    data = data.split(' ')
    chunked_inputs = [data[i:i+1024] for i in range(0,len(data),1024)]
    summary = ''
    
    # Determine the minimum and maximum chunk length
    min_chunk_length = min_length // len(chunked_inputs)
    max_chunk_length = max_length // len(chunked_inputs)
    
    # Get input for each chunk
    for i, chunk in enumerate(chunked_inputs):
        print(f"Summarizing chunk {i+1} of {len(chunked_inputs)}")
        chunk = ' '.join(chunk)
        chunk_summary = truncate_summary(chunk,model,tokenizer,min_chunk_length,max_chunk_length)
        chunk_summary = chunk_summary.split('</s>')[-2].split('<s>')[-1].strip()
        summary += (' '+chunk_summary)
    
    # Save the summary to a file
    save_file_path = os.path.join(summary_folder, get_league(sport, lower=True) + "_summary.txt")
    with open(save_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)

def summarize_summaries(sport: Sport, min_length: int = 1000, max_length: int = 2250, summary_folder: str = SUMMARY_FOLDER_PATH, save_folder: str = FINAL_SUMMARIES_FOLDER_PATH):
    """Takes the summaries for the sport and does another round of summarization to decrease the length even further. 
    This is most useful for decreasing the number of tokens so an all-encompassing summary can be used in a single GPT query. 

    Args:
        sport (Sport): The sport to summarize the summaries for
        min_length (int, optional): The minimum length of the summary. Defaults to 1000.
        max_length (int, optional): The maximum length of the summary. Defaults to 2250.
        summary_folder (str, optional): Path to the folder where the summaries are stored. Defaults to SUMMARY_FOLDER_PATH.
        save_folder (str, optional): Path to the folder where the new summaries will be saved. Defaults to FINAL_SUMMARIES_FOLDER_PATH.
    """
    # Load the summary
    big_summary = load_summary_data(sport, folder_path=summary_folder)
    
    # initialize model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    
    # Separate the  text into chunks
    big_summary = big_summary.split(' ')
    chunked_inputs = [big_summary[i:i+1024] for i in range(0,len(big_summary),1024)]
    summary = ''
    
    # Determine the minimum and maximum chunk length
    min_chunk_length = min_length // len(chunked_inputs)
    max_chunk_length = max_length // len(chunked_inputs)
    
    # Get input for each chunk
    for i, chunk in enumerate(chunked_inputs):
        print(f"Summarizing chunk {i+1} of {len(chunked_inputs)}")
        chunk = ' '.join(chunk)
        chunk_summary = truncate_summary(chunk,model,tokenizer,min_chunk_length,max_chunk_length)
        chunk_summary = chunk_summary.split('</s>')[-2].split('<s>')[-1].strip()
        summary += (' '+chunk_summary)
    
    # Save the summary to a file
    save_file_path = os.path.join(save_folder, get_league(sport, lower=True) + "_summary_final.txt")
    with open(save_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)

def truncate_summary(input_text: str, model: AutoModelForSeq2SeqLM, tokenizer: AutoTokenizer, min_length: int, max_length: int):
    """A helper function to truncate the summary to a certain length

    Args:
        input_text (str): The text to summarize
        model (AutoModelForSeq2SeqLM): The model that is used to summarize the text
        tokenizer (AutoTokenizer): The tokenizer model that is used to tokenize the text
        min_length (int): The minimum length of the summary
        max_length (int): The maximum length of the summary

    Returns:
        str: The summarized text
    """
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, length_penalty=1.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0])
    
###############################
##### Load Data Functions #####
###############################
def load_processed_data(sport: Sport, folder_path: str = PROCESSED_DATA_FOLDER_PATH):
    """Loads the processed data from the processed_data folder

    Args:
        sport (Sport): The sport to load the data for
        folder_path (str, optional): The folder to load the data from. Defaults to PROCESSED_DATA_FOLDER_PATH.
        
    Returns:
        str: The processed text data
    """
    data_file = os.path.join(folder_path, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def load_text_data(sport: Sport, folder_path: str = TEXT_DATA_FOLDER_PATH):
    """Loads the text data from the given data txt file

    Args:
        sport (Sport): The sport to load the data for
        folder_path (str, optional): The folder to load the data from. Defaults to PROCESSED_DATA_FOLDER_PATH.

    Returns:
        data (str): The processed text data as a string
    """
    data_file = os.path.join(folder_path, get_league(sport, lower=True) + "_rules.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def load_summary_data(sport: Sport, folder_path: str = SUMMARY_FOLDER_PATH):
    """Loads the summary data from the given data txt file

    Args:
        sport (Sport): The sport to load the data for
        folder_path (str, optional): The folder to load the data from. Defaults to PROCESSED_DATA_FOLDER_PATH.

    Returns:
        data (str): The processed text data as a string
    """
    data_file = os.path.join(folder_path, get_league(sport, lower=True) + "_summary.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

#################
##### Main ######
#################
if __name__ == "__main__":
    ##################################
    # Pipleline from start to finish #
    ##################################
    
    # Indicate the data folders
    raw_folder = os.path.join('..', RAW_DATA_FOLDER_PATH)
    text_folder = os.path.join('..', TEXT_DATA_FOLDER_PATH)
    processed_folder = os.path.join('..', PROCESSED_DATA_FOLDER_PATH)
    document_store_folder = os.path.join('..', DOCUMENT_STORE_FOLDER_PATH)
    summary_folder = os.path.join('..', SUMMARY_FOLDER_PATH)
    
    # Convert the pdf data to text data
    print("Converting the pdf data to text data...")
    print("Converting the NFL data...")
    pdf_to_text(filename='2022-nfl-rulebook-final.pdf', sport=Sport.FOOTBALL, origin_folder=raw_folder, dest_folder=text_folder)
    print("Converting the NHL data...")
    pdf_to_text(filename='2022-nhl-rulebook.pdf', sport=Sport.HOCKEY, origin_folder=raw_folder, dest_folder=text_folder)
    print("Converting the NBA data...")
    pdf_to_text(filename='2022-2023-NBA-RULE-BOOK.pdf', sport=Sport.BASKETBALL, origin_folder=raw_folder, dest_folder=text_folder)
    print("Converting the WNBA data...")
    pdf_to_text(filename='2022-WNBA-RULE-BOOK-FINAL.pdf', sport=Sport.WOMENS_BASKETBALL, origin_folder=raw_folder, dest_folder=text_folder)
    
    # Scrape the ultimate data
    print("Scraping the Ultimate Data...")
    scrape_ultimate_data(sport=Sport.ULTIMATE, dest_folder=text_folder)
    
    # Process the text data
    for sport in Sport:
        print(f"Processing {sport.value} Rules...")
        process_text(sport, origin_folder=text_folder, dest_folder=processed_folder)
        
        print(f"Chunking {sport.value} Rules...")
        chunk_processed_data(sport, split_length=250, split_overlap=50, processed_data_folder=processed_folder, document_folder=document_store_folder)
        
        print(f"Summarizing {sport.value} Rules...")
        summarize_rules(sport, min_length=1000, max_length=10_000, processed_folder=processed_folder, summary_folder=summary_folder)
        
        print(f"Further Summarizing {sport.value} Rules...")
        summarize_summaries(sport)