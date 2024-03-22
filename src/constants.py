# Imports
import os

# Folders
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
PROCESSED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

# Text Processing
ACCEPTABLE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,./<>?~"\' '