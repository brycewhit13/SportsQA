# Imports
import os
import requests

from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader


from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER, FAISS_DB_FOLDER
from src.constants import ACCEPTABLE_CHARS

# Ultimate Classes
class USAU_Ultimate(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'usau_rulebook_2024.txt'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'USAU_processed.txt'),
            online_link = 'https://usaultimate.org/rules/', 
            league_name = 'USAU', 
            sport_name = 'Ultimate Frisbee'
        )
    
    
    def load_raw_text(self):
        """
        Loads the raw text and returns it as a string
        """
        try:
            with open(self.raw_data_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print('File not found, scraping data from the web')
            # Scrape the data from the web
            raw_text = self.scrape_data()
            
            # Save the raw text to a file before returning it
            with open(self.raw_data_path, 'w') as f:
                f.write(raw_text)
            return raw_text
    
    
    def scrape_data(self):
        """
        Scrapes the rules from the web and returns them as a string
        """
        # Create the raw text file for later
        raw_text = ''

        # Request the webpage
        html = requests.get(self.online_link)

        # Parse the html and save the text
        soup = BeautifulSoup(html.content, 'html.parser')
        
        # Get the main rules
        main_rules = soup.find(name='ol', attrs={'class':'main-rules'}).find_all(name='li')
        for section in main_rules:
            if section.text not in raw_text:
                raw_text += section.text
            
        # Get the appendices
        appendices = soup.find(name='ol', attrs={'class':'appendices'}).find_all(name='li')
        for section in appendices:
           if section.text not in raw_text:
                raw_text += section.text
        
        return raw_text
    
    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = raw_text.replace('’', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('…', '...')
        
        # Remove any remaining non-standard characters completely
        unencoded_characters = set(processed_text).difference(set(ACCEPTABLE_CHARS))
        for char in unencoded_characters:
            processed_text = processed_text.replace(char, ' ')
        
        # Save the processed text to be retrieved later
        with open(self.processed_data_path, 'w') as f:
            f.write(processed_text)
    
    
    def embed_document(self):
        # Load the raw text with the document loader
        docs = TextLoader(self.processed_data_path).load()
        
        # Chunk the text for the FAISS db
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
        chunked_docs = text_splitter.split_documents(docs)
        
        # Initialize the embedding model
        embedding_model = MistralAIEmbeddings(mistral_api_key=os.environ['MISTRAL_API_KEY'])
        
        # Create and save the FAISS db
        db = FAISS.from_documents(chunked_docs, embedding_model)
        db.save_local(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{self.league_name}'))
