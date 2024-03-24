# Imports
import streamlit as st

from src.faiss_db import load_faiss_db
from src.inference import query_llm, load_llm_pipeline
from src.Sports import Sports

# Constants
SPORT_LEAGUE_MAPPING = {
    'Football': ['NFL'],
    'Basketball': ['NBA', 'WNBA'],
    'Hockey': ['NHL'],
    'Ultimate Frisbee': ['USAU'],
}

LEAGUE_TO_ENUM_MAPPING = {
    'NFL': Sports.NFL,
    'NBA': Sports.NBA,
    'WNBA': Sports.WNBA,
    'NHL': Sports.NHL,
    'USAU': Sports.USAU,
}
        

def main():
    # Create a title for the app
    st.title('Sports Q&A')
    
    # Create two dropdowns side by side: One to select the sport and one to select the league
    col1, col2 = st.columns(2)
    with col1:
        sport = st.selectbox('Select a sport', ['🏈 Football', '🏀 Basketball', '🏒 Hockey', '🥏 Ultimate Frisbee'])
    with col2:
        league = st.selectbox('Select a league', SPORT_LEAGUE_MAPPING[' '.join(sport.split(' ')[1:])])
    
    # Create two text boxes: One to ask a question and one where the response will be displayed
    question_box = st.text_area('Ask a question', max_chars=250)
    response_box = st.text_area('Response', max_chars=250, disabled=True)
    
    # Create a button to submit the question
    if st.button('Submit'):
        response_box.text(f'You asked: {question_box}')
        

if __name__ == '__main__':
    main()