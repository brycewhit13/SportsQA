# Imports
from Sports import Sport


def process_raw_text(sport: Sport):
    sport_object = sport.value
    
    # Load the raw text
    raw_text = sport_object.load_raw_text()
    
    # Lowercase text
    processed_text = raw_text.lower()
    # Remove any spots with more than one space
    processed_text = ' '.join(processed_text.split())
    # Fix encodings for apostrophe, open/close double quotes, and hypens
    #processed_text = processed_text.replace('’', '\'')
    #processed_text = processed_text.replace('“', '"')
    #processed_text = processed_text.replace('”', '"')
    #processed_text = processed_text.replace('–*', '-')
    
    # Check if there are any unencoded characters
    unencoded_characters = set(processed_text).difference(set('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,./<>?~ '))
    print(unencoded_characters)
    
    # Save the text
    with open(sport_object.processed_data_path, 'w') as f:
        f.write(processed_text)

def process_raw_text_all():
    for sport in Sport:
        process_raw_text(sport=sport)
        


if __name__ == '__main__':
    process_raw_text(sport=Sport.USAU)