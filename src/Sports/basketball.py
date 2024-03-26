# imports
import os

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

from src.Sports.base import BaseSport
from src.constants import RAW_DATA_FOLDER, PROCESSED_DATA_FOLDER, FAISS_DB_FOLDER
from src.constants import ACCEPTABLE_CHARS

# Basketball Classes
class NBA_Basketball(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'nba_rulebook_2023_2024.pdf'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'NBA_processed.txt'),
            online_link = 'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf', 
            league_name = 'NBA', 
            sport_name = 'Basketball'
        )
    
    
    def load_raw_text(self):
        """
        Load the raw data and return it as a string
        """  
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text
    
    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = raw_text.replace('’', '\'')
        processed_text = processed_text.replace('‘', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        processed_text = processed_text.replace('°', ' degrees') # Degree symbol
        
        # Replace fractions
        processed_text = processed_text.replace('¾', '3/4')
        processed_text = processed_text.replace('½', '1/2')
        
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


class WNBA_Basketball(BaseSport):
    
    def __init__(self):
        # Call the parent class with these values
        super().__init__(
            raw_data_path = os.path.join(RAW_DATA_FOLDER, 'wnba_rulebook_2022.pdf'),
            processed_data_path = os.path.join(PROCESSED_DATA_FOLDER, 'WNBA_processed.txt'),
            online_link = 'https://cdn.wnba.com/league/2022/05/2022-WNBA-RULE-BOOK-FINAL.pdf', 
            league_name = 'WNBA', 
            sport_name = 'Basketball'
        )        
    
    
    def load_raw_text(self):
        """
        Load the raw data and return it as a string
        """
        # Instantiate PDF Reader
        pdf_reader = PdfReader(self.raw_data_path)
        
        # Extract Text
        raw_text = ''
        for page in pdf_reader.pages:
            raw_text += page.extract_text()
        return raw_text
    
    
    def process_text(self):
        # Load the raw text
        raw_text = self.load_raw_text()
        
        # Fix encodings for apostrophe, open/close double quotes, and hypens
        processed_text = raw_text.replace('’', '\'')
        processed_text = processed_text.replace('‘', '\'')
        processed_text = processed_text.replace('“', '"')
        processed_text = processed_text.replace('”', '"')
        processed_text = processed_text.replace('–', '-')
        processed_text = processed_text.replace('—', '-')
        
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