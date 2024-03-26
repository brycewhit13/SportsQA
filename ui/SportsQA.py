# Imports
import streamlit as st

from src.Sports import Sports
from src.faiss_db import load_faiss_db, query_faiss_db, query_faiss_with_rerank
from src.inference import construct_prompt, invoke_llm, stream_llm, context_required

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

def clear_chat_history():
    if "messages" in st.session_state:
        st.session_state.messages = []

def main():
    # Create a title for the app
    st.title('Sports Rules Q&A')
    
    # Create two dropdowns side by side: One to select the sport and one to select the league
    col1, col2 = st.columns(2)
    with col1:
        sport = st.selectbox('Select a sport', ['🏈 Football', '🏀 Basketball', '🏒 Hockey', '🥏 Ultimate Frisbee'], on_change=clear_chat_history)
    with col2:
        league = st.selectbox('Select a league', SPORT_LEAGUE_MAPPING[' '.join(sport.split(' ')[1:])], on_change=clear_chat_history)
    
    # Link the rulebook of the sport they are on
    sport_enum = LEAGUE_TO_ENUM_MAPPING[league]
    st.markdown(f'Check out the [Offical {sport_enum.value.league_name} Rulebook]({sport_enum.value.online_link})')
    
    # Create the chat message box and introduce ourself
    st.chat_message('assistant').write("""Welcome, I am here to answer any questions you may have about the official rules of different sports. 
                            Select a sport and corresponding league from the drop-down menus above and then feel free to ask me anything!""")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if question := st.chat_input("Ask a question", max_chars=250):
        # Display user message in chat message container
        st.chat_message('User').write(question)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})

        # Determine if we need to get context with RAG or not
        if context_required(sport=sport_enum, query=question, chat_history=st.session_state.messages):
            # Load the appropriate FAISS db
            db = load_faiss_db(sport=sport_enum)
            context_list = query_faiss_with_rerank(db, query=question)
        else:
            context_list = None
        
        # Get a response from the LLM
        prompt = construct_prompt(sport=sport_enum,
                                  query=question,
                                  context_list=context_list,
                                  chat_history=st.session_state.messages)

        #response_stream = stream_llm(prompt=prompt)
        response = invoke_llm(prompt=prompt)
        st.chat_message('assistant').write(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()