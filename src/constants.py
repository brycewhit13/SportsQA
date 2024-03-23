# Imports
import os

# Folders
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
PROCESSED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
FAISS_DB_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss')

# Text Processing
ACCEPTABLE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,./<>?~"\'\n '

# FAISS DB
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"