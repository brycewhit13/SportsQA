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

# LLM
LLM_MODEL_NAME = 'mistralai/Mistral-7B-Instruct-v0.2'
PROMPT_TEMPLATE = \
'''
[INST]
Here is some important context which can help answer the question asked by the user.
Make sure to not make anything up to answer the question if it is not provided in the context.

<context>
{context}
</context>

User Question: {question}
[/INST]
'''