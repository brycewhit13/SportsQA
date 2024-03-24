# Imports
from time import time

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory

from src.Sports import Sports
from src.faiss_db import load_faiss_db, query_faiss_db
from constants import LLM_MODEL_NAME, PROMPT_TEMPLATE

def timer_func(func): 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 


@timer_func
def load_llm_pipeline():    
    # Create the LLM pipeline
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME)
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_new_tokens=1000)
    return HuggingFacePipeline(pipeline=pipe)

@timer_func
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

@timer_func
def add_query_to_prompt(query: str, prompt: str):
    return prompt.replace('{question}', query)

@timer_func
def query_llm(llm: HuggingFacePipeline, db, query: str):
    # Get the context from the db
    context_list = query_faiss_db(db, query)
    
    # Add the query and the context to the prompt
    prompt = add_context_to_prompt(context_list=context_list, prompt=PROMPT_TEMPLATE)
    prompt = add_query_to_prompt(query=query, prompt=prompt)
    
    # Return the response from the LLM
    return llm.invoke(prompt)

if __name__ == '__main__':
    # Load the db and llm pipeline
    llm = load_llm_pipeline()
    db = load_faiss_db(Sports.NBA)
    
    # Query the llm
    result = query_llm(llm, db, query='How many players are on the floor at one time?')
    print(result)