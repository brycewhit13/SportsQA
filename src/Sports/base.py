# Imports
import os

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

from src.constants import FAISS_DB_FOLDER

# Parent sports class
class BaseSport():
    
    def __init__(self, raw_data_path, processed_data_path, online_link, league_name, sport_name):
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        self.online_link = online_link
        self.league_name = league_name
        self.sport_name = sport_name
    
    def load_document(self):
        """
        Loads the document using the appropriate langchain document loader and returns the result
        """
        if self.processed_data_path.endswith('.pdf'):
            return PyPDFLoader(self.processed_data_path).load_and_split()
        elif self.processed_data_path.endswith('.txt'):
            return TextLoader(self.processed_data_path).load()
        else:
            raise ValueError('Document type not supported')
    
    
    def load_processed_text(self):
        with open(self.processed_data_path, 'r') as f:
            return f.read()
    
    
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