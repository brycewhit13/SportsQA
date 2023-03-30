####################################################################
# Filename: get_data.py                                            #
# Author: Bryce Whitney                                            #
# Last Edit: 3/30/2023                                             #
#                                                                  #
# Description: Contains functions for generating the data and      #
# uploading / downloading it from the Azure blob storage system.   #
####################################################################

# Imports
import os
import string
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from Sport import Sport, get_league
from constants import RAW_DATA_FOLDER_PATH, TEXT_DATA_FOLDER_PATH, PROCESSED_DATA_FOLDER_PATH, STOPWORDS_SET

# Constants
STORAGE_ACCOUNT_NAME = "sportsrulesdb"
CONTAINER_NAME = "sports-data"

##### Establish Azure Connection #####
def establish_connection():
    # Create the BlobServiceClient and ContainerClient objects
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    # Return the clients
    return blob_service_client, container_client

##### Download Functions #####
def download_raw_data(container_client, download_folder = os.path.join("..", "data", "raw_data2")):
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

def download_text_data(container_client, download_folder = os.path.join("..", "data", "text_data2")):
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

def download_processed_data(container_client, download_folder = os.path.join("..", "data", "processed_data2")):
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
            
def download_all_data(container_client):
    print("Downloading the raw data...")
    download_raw_data(container_client)
    
    print("Downloading the text data...")
    download_text_data(container_client)
    
    print("Downloading the processed data...")
    download_processed_data(container_client)
    
    
##### Upload Functions #####
def upload_file_to_azure(container_client, file_path, upload_folder):
    # Get the file name
    file_name = os.path.split(file_path)[1]
    
    # Upload the file
    with open(file=file_path, mode="rb") as data:
        container_client.upload_blob(name=os.path.join(upload_folder, file_name), data=data)
        
        
def upload_folder_to_azure(container_client, folder_path, upload_folder):
    # List the files in the folder
    file_list = os.listdir(folder_path)
    
    # For each file
    for file_name in file_list:
        # Get the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Upload the file
        upload_file_to_azure(container_client, file_path, upload_folder)
        
        
##### Data Generation Functions #####
def pdf_to_text(filename: str, sport: Sport, start_page: int = 0, end_page: int = None):
    """Loads text from a pdf file and saves it to a txt file. You can specify the start and end pages to load
    and the resulting text is stored in the text_data folder with the output_name as the file name.

    Args:
        filename (str): the filename in the raw data folder
        output_name (str): Output file name
        start_page (int, optional): the first page to load. Defaults to 0.
        end_page (int, optional): the last page to load. Defaults to None.
    """
    # Load the rulebook from the PDF
    data = PdfReader(os.path.join(RAW_DATA_FOLDER_PATH, filename))
    
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
    with open(os.path.join(TEXT_DATA_FOLDER_PATH, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

def scrape_ultimate_data(sport: Sport = Sport.ULTIMATE):
    """Scrapes USAU ultimate rules from the website and saves to a txt file
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
    with open(os.path.join(TEXT_DATA_FOLDER_PATH, output_name), 'w', encoding='utf-8') as f:
        f.write(text)

##### Text Preprocessing Functions #####
def process_text(sport: Sport, remove_stopwords: bool = False, remove_punctuation: bool = False):
    """Processes the text data from the text_data folder and stores the results in the processed_data folder.

    Args:
        data_file (str): The file name of the data to process
        output_file (str): The file name to store the processed data
    """
    # Read in the data
    data_file = os.path.join(TEXT_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules.txt")
    data = _load_text_data(data_file)
    
    # Make everything lowercase
    data_processed = data.lower()
    # Replace non alphanumeric characters with empty strings
    data_processed = data_processed.replace("[^a-zA-Z0-9_]", "")
    # Remove Stopwords and Punctuation if necessary
    if(remove_stopwords == True):
        data_processed = _remove_stopwords(data_processed)
    if(remove_punctuation == True):
        data_processed = _remove_punctuation(data_processed)
    if(remove_stopwords == False and remove_punctuation == False):
        data_processed = " ".join([word for word in data_processed.split()])
    
    # Save the processed data to the output file
    output_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(data_processed)    
    
    
def load_processed_data(sport: Sport):
    """Loads the processed data from the processed_data folder

    Args:
        sport (Sport): The sport to load the data for

    Returns:
        str: The processed text data
    """
    data_file = os.path.join(PROCESSED_DATA_FOLDER_PATH, get_league(sport, lower=True) + "_rules_processed.txt")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

##### Helper Functions #####
def _remove_stopwords(data):
    """Removes stopwords from the data

    Args:
        data (str): The data to remove stopwords from

    Returns:
        data_processed (str): The data with stopwords removed
    """
    data_processed = " ".join([word for word in data.split() if word not in STOPWORDS_SET])
    return data_processed

def _remove_punctuation(data):
    """Removes punctuation from the data

    Args:
        data (str): The data to remove punctuation from

    Returns:
        data_processed (str): The data with punctuation removed
    """
    data_processed = " ".join([word for word in data.split() if word not in string.punctuation])
    return data_processed

def _load_text_data(data_file: str):
    """Loads the text data from the given data txt file

    Args:
        data_file (str): The file name of the data to load

    Returns:
        data (str): The processed text data as a string
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


##### Main ######
if __name__ == "__main__":
    # Establish the connection
    #blob_service_client, container_client = establish_connection()
    
    # Download the data
    #download_all_data(container_client)
    
    ##################################
    # Pipleline from start to finish #
    ##################################
    
    # Convert the pdf data to text data
    print("Converting the pdf data to text data...")
    print("Converting the NFL data...")
    pdf_to_text(filename='2022-nfl-rulebook-final.pdf', sport=Sport.FOOTBALL)
    print("Converting the NHL data...")
    pdf_to_text(filename='2022-nhl-rulebook.pdf', sport=Sport.HOCKEY)
    print("Converting the NBA data...")
    pdf_to_text(filename='2022-2023-NBA-RULE-BOOK.pdf', sport=Sport.BASKETBALL)
    print("Converting the WNBA data...")
    pdf_to_text(filename='2022-WNBA-RULE-BOOK-FINAL.pdf', sport=Sport.WOMENS_BASKETBALL)
    print("Converting the ICC data...")
    pdf_to_text(filename='2020-ICC-Playing-Handbook.pdf', sport=Sport.CRICKET)
    
    # Scrape the ultimate data
    print("Scraping the Ultimate Data...")
    scrape_ultimate_data(sport=Sport.ULTIMATE)
    
    # Process the text data
    for sport in Sport:
        print(f"Processing {sport.value} Rules...")
        process_text(sport)
    
    # Upload the processed data to blob storage
    blob_service_client, container_client = establish_connection()
    upload_folder_to_azure(container_client=container_client, folder_path=PROCESSED_DATA_FOLDER_PATH, upload_folder='processed-data')
    
    
