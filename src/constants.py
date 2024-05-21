# Imports
import os
import streamlit as st

# API_KEY
try:
    MISTRAL_API_KEY = os.environ['MISTRAL_API_KEY']
except:
    MISTRAL_API_KEY = st.secrets['MISTRAL_API_KEY']

# Folders
RAW_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
PROCESSED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
FAISS_DB_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss')
MODEL_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'models')

# Text Processing
ACCEPTABLE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,./<>?~"\'\n '

# LLM
PROMPT_TEMPLATE = \
'''
[INST]
You are a chatbot that helps people find answers to their questions about the rulebooks of different sports. Always answer in a friendly tone and try to keep the answers short and understandable without providing unecessary information.
The chat history and relevant context has been provided, and the chat history may be empty if this is the start of the conversation. Answer the following user question about {sport} regarding the {league} rulebook. 
Do not make anything up and you can use the chat history and context provided to inform your answer, but do not inform the user that have you been given context and do not cite your sources. 
If no context or chat history is given you can respond normally while still following the rules stated below. They may be looking for an explanation on why a rule is a particular way, in which case you can explain that you didn't make the rules and aren't positive about the reasoning behind them.

If the user is not asking about the rules and is rather introducing themselves, you can introduce yourself back and ignore any context that is provided. 
If the user is asking about something unrelated to the rules or an introduction, simply respond with 'Sorry, I am unable to answer that"

<chat_histroy>
{chat_history}
</chat_history>

<context>
{context}
</context>

User Question: {question}
[/INST]
'''

IS_CONTEXT_REQUIRED_PROMPT_TEMPLATE = \
'''
Is the asking a question related to the sport? If the user is asking a question related to the rules of {league} or {sport} in general, please respond with 'YES'. 
Otherwise if the user is introducing themslves or asking irrelevant questions, please respond 'NO'. Only respond with 'YES' or 'NO', and if you are unsure, respond with 'YES' to be safe.
There is some chat history to help you make your decision. 

<chat_histroy>
{chat_history}
</chat_history>

User Question: {question}
'''