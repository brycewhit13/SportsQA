####################################################################
# Filename: get_data.py                                            #
# Author: Bryce Whitney                                            #
# Last Edit: 4/4/2023                                              #
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

from azure.storage.blob import BlobServiceClient

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

###########################
##### Azure Functions #####
###########################

##### Download Function #####
def establish_connection(container_name=CONTAINER_NAME):
    """Establishes a connection to the Azure blob storage system
    Args:
        container_name (str, optional): Name of the container to connect to. Defaults to "sports-data".
        
    Returns:
        tuple: A tuple containing the BlobServiceClient and ContainerClient objects
    """
    # Create the BlobServiceClient and ContainerClient objects
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(container_name)
    
    # Return the clients
    return blob_service_client, container_client

def download_raw_data(container_client, download_folder = os.path.join("..", "data", "raw_data")):
    """Downloads the raw data from the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        download_folder (str, optional): path. Defaults to "../data/raw_data").
    """
    # If download folder doesn't exist, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # List the blobs in the raw-data container
    blob_list = container_client.list_blobs(name_starts_with="raw-data")
    
    # For each file
    for blob in blob_list:
        file_name = os.path.split(blob.name)[1]
        download_path = os.path.join(download_folder, file_name)

        # Download the file
        with open(file=download_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())

def download_text_data(container_client, download_folder = os.path.join("..", "data", "text_data")):
    """Downloads the text data from the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        download_folder (str, optional): path. Defaults to "../data/text_data").
    """
    # If download folder doesn't exist, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    # List the blobs in the text-data container
    blob_list = container_client.list_blobs(name_starts_with="text-data")
    
    # For each file
    for blob in blob_list:
        file_name = os.path.split(blob.name)[1]
        download_path = os.path.join(download_folder, file_name)

        # Download the file
        with open(file=download_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())

def download_processed_data(container_client, download_folder = os.path.join("..", "data", "processed_data")):
    """Downloads the processed data from the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        download_folder (str, optional): path. Defaults to "../data/processed_data").
    """
    # If download folder doesn't exist, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    # List the blobs in the processed-data container
    blob_list = container_client.list_blobs(name_starts_with="processed-data")
    
    # For each file
    for blob in blob_list:
        file_name = os.path.split(blob.name)[1]
        download_path = os.path.join(download_folder, file_name)

        # Download the file
        with open(file=download_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())

def download_document_store(container_client, download_folder = DOCUMENT_STORE_FOLDER_PATH):
    """Downloads the document store from the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        download_folder (str, optional): path. Defaults to DOCUMENT_STORE_FOLDER_PATH).
    """
    # If download folder doesn't exist, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    # List the blobs in the document-store container
    blob_list = container_client.list_blobs(name_starts_with="document-store")
    
    # For each file
    for blob in blob_list:
        file_name = os.path.split(blob.name)[1]
        download_path = os.path.join(download_folder, file_name)

        # Download the file
        with open(file=download_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())
            
def download_all_data(container_client):
    """Downloads all of the data from the Azure blob storage system
    
    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
    """
    
    print("Downloading the raw data...")
    download_raw_data(container_client)
    
    print("Downloading the text data...")
    download_text_data(container_client)
    
    print("Downloading the processed data...")
    download_processed_data(container_client)
    
    print("Downloading Document Store...")
    download_document_store(container_client)
    
    print("Download Complete!")
    

##### Upload Functions #####
def upload_file_to_azure(container_client, file_path, upload_folder):
    """Uploads a file to the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        file_path (str): path to the file to upload
        upload_folder (str): name of the folder to upload the file to
    """
    # Get the file name
    file_name = os.path.split(file_path)[1]
    
    # Upload the file
    with open(file=file_path, mode="rb") as data:
        container_client.upload_blob(name=os.path.join(upload_folder, file_name), data=data)
        
        
def upload_folder_to_azure(container_client, folder_path, upload_folder):
    """Uploads a folder to the Azure blob storage system

    Args:
        container_client (ContainerClient): ContainerClient object connected to the azure blob storage system
        folder_path (str): path to the folder to upload
        upload_folder (str): name of the folder to upload the file to
    """
    # List the files in the folder
    file_list = os.listdir(folder_path)
    
    # For each file
    for file_name in file_list:
        # Get the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Upload the file
        upload_file_to_azure(container_client, file_path, upload_folder)
        
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


##### Main ######
if __name__ == "__main__":
    ##################################
    # Pipleline from start to finish #
    ##################################
    
    # Indicate the data folders
    raw_folder = os.path.join('..', RAW_DATA_FOLDER_PATH)
    text_folder = os.path.join('..', TEXT_DATA_FOLDER_PATH)
    processed_folder = os.path.join('..', PROCESSED_DATA_FOLDER_PATH)
    document_store_folder = os.path.join('..', DOCUMENT_STORE_FOLDER_PATH)
    
    '''
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
    '''
    # Process the text data
    for sport in Sport:
        print(f"Processing {sport.value} Rules...")
        process_text(sport, origin_folder=text_folder, dest_folder=processed_folder)
        
        print(f"Chunking {sport.value} Rules...")
        chunk_processed_data(sport, split_length=2000, split_overlap=100, processed_data_folder=processed_folder, document_folder=document_store_folder)
        