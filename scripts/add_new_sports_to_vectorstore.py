import os

from src.Sports import Sports
from src.faiss_db import embed_single_document
from src.constants import FAISS_DB_FOLDER

if __name__ == '__main__':
    # Loop through all the sports:
    for sport in Sports:
        if not os.path.exists(os.path.join(FAISS_DB_FOLDER, f'faiss_index_{sport.value.league_name}')):
            embed_single_document(sport=sport)