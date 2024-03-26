import os

from src.Sports import Sports
from src.constants import PROCESSED_DATA_FOLDER

if __name__ == '__main__':
    for sport in Sports:
        if not os.path.exists(os.path.join(PROCESSED_DATA_FOLDER, f'{sport.value.league_name}_processed.txt')):
            sport.process_text()
