# Imports
from langchain_community.document_loaders import TextLoader, PyPDFLoader

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