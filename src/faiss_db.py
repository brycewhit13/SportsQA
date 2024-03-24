# Imports
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.Sports import Sports
from src.constants import FAISS_DB_FOLDER, EMBEDDING_MODEL_NAME

def embed_single_document(sport: Sports):
    # Load the document for the sport
    sport_obj = sport.value
    docs = sport_obj.load_document()
    
    # Chunk the text for the FAISS db
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunked_docs = text_splitter.split_documents(docs)
    
    # Initialize the embedding model
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Create and save the FAISS db
    db = FAISS.from_documents(chunked_docs, embedding_model)
    db.save_local(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{sport_obj.league_name}'))
    
    
def embed_all_documents():
    for sport in Sports:
        embed_single_document(sport)


def load_faiss_db(sport: Sports):
    # Get info needed to load the db and then return the loaded db
    sport_obj = sport.value
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return FAISS.load_local(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{sport_obj.league_name}'), embedding_model, allow_dangerous_deserialization=True)


def query_faiss_db(db, query: str, k: int = 3):
    retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': k})
    return retriever.invoke(query)
