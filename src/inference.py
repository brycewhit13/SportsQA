# Imports
import os

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mistralai.chat_models import ChatMistralAI

from src.Sports import Sports
from src.faiss_db import load_faiss_db, query_faiss_db
from src.constants import PROMPT_TEMPLATE, IS_CONTEXT_REQUIRED_PROMPT_TEMPLATE

def initialize_mistral_chat():
    return ChatMistralAI(mistral_api_key=os.environ['MISTRAL_API_KEY'], model='open-mistral-7b', temperature=0.2, safe_mode=True)


def add_context_to_prompt(context_list, prompt: str):
    # Add the context and question to the prompt
    for i, context in enumerate(context_list):
        # Leave room for more replacements if we haven't reached the last one
        if i != len(context_list) - 1:
            prompt = prompt.replace('{context}', f'{i+1}) {context.page_content}\n\n{{context}}')
        else:
            prompt = prompt.replace('{context}', f'{i+1}) {context.page_content}')
    
    # Return the updated prompt
    return prompt


def remove_context_from_prompt(prompt: str):
    prompt = prompt.replace('<context>', '')
    prompt = prompt.replace('{context}', '')
    prompt = prompt.replace('</context>', '')
    return prompt
    


def add_query_to_prompt(query: str, prompt: str):
    return prompt.replace('{question}', query)


def add_conversation_histroy_to_prompt(chat_histroy: list, prompt: str):
    # Convert the chat history to (You and User)
    final_chat_list = []
    for chat in chat_histroy:
        if chat['role'] == 'user':
            final_chat_list.append(f'User: {chat["content"]}')
        elif chat['role'] == 'assistant':
            final_chat_list.append(f'You: {chat["content"]}')
        
    # Add the final chat list
    return prompt.replace('{chat_history}', '\n'.join(final_chat_list))

def add_sport_to_prompt(sport: Sports, prompt: str):
    return prompt.replace('{sport}', sport.value.sport_name).replace('{league}', sport.value.league_name)


def construct_prompt(sport: Sports, query: str = '', context_list: list = None, chat_history: list = None):
    # Add in each of the components
    prompt = add_sport_to_prompt(sport=sport, prompt=PROMPT_TEMPLATE)
    prompt = add_query_to_prompt(query=query, prompt=prompt)
    if context_list is not None:
        prompt = add_context_to_prompt(context_list=context_list, prompt=prompt)
    else:
        prompt = remove_context_from_prompt(prompt=prompt)
    if chat_history is not None:
        prompt = add_conversation_histroy_to_prompt(chat_histroy=chat_history, prompt=prompt)
    
    # Return the result
    return prompt

def invoke_llm(prompt: str):
    chat = initialize_mistral_chat()
    return chat.invoke(prompt).content

def stream_llm(prompt: str):
    chat = initialize_mistral_chat()
    return chat.stream(prompt)


def context_required(sport: Sports, query: str, chat_history: list):
    chat = initialize_mistral_chat()
    prompt = add_sport_to_prompt(sport=sport, prompt=IS_CONTEXT_REQUIRED_PROMPT_TEMPLATE)
    prompt = add_query_to_prompt(query=query, prompt=prompt)
    prompt = add_conversation_histroy_to_prompt(chat_histroy=chat_history, prompt=prompt)
    response = chat.invoke(prompt)
    
    if 'YES' in response.content.split()[0]:
        return True
    elif 'NO' in response.content.split()[0]:
        return False
    else:
        raise ValueError("Asking if context is required yielded an invalid result")