# Imports
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from flashrank import Ranker

from src.Sports import Sports
from src.constants import FAISS_DB_FOLDER, MODEL_FOLDER, MISTRAL_API_KEY


def embed_single_document(sport: Sports):
    # Load the document for the sport
    sport_obj = sport.value
    docs = sport_obj.load_document()
    
    # Chunk the text for the FAISS db
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
    chunked_docs = text_splitter.split_documents(docs)
    
    # Initialize the embedding model
    embedding_model = MistralAIEmbeddings(mistral_api_key=MISTRAL_API_KEY)
    
    # Create and save the FAISS db
    db = FAISS.from_documents(chunked_docs, embedding_model)
    db.save_local(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{sport_obj.league_name}'))
    
    
def embed_all_documents():
    for sport in Sports:
        embed_single_document(sport)


def load_faiss_db(sport: Sports):
    # Get info needed to load the db and then return the loaded db
    sport_obj = sport.value
    embedding_model = MistralAIEmbeddings(mistral_api_key=MISTRAL_API_KEY)
    return FAISS.load_local(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{sport_obj.league_name}'), embedding_model, allow_dangerous_deserialization=True)

def query_faiss_db(db, query: str, k: int = 3):
    retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': k})
    return retriever.invoke(query)


def query_faiss_with_rerank(db, query: str):
    compressor = FlashrankRerank(client=Ranker(model_name='ms-marco-MiniLM-L-12-v2', cache_dir=MODEL_FOLDER))
    retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': 15})
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    return compression_retriever.get_relevant_documents(query)
