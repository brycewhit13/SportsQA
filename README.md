# Sports Rule Q&A

## Description

In professional sports, the rules are constantly being tweaked, whether it be to increase marketability, increase player safety, or simply experiment with a new rule. As a casual fan of many sports, I find it difficult to keep up-to-date with all the changes year to year. This inspired me to create this chatbot where I can go and ask any questions I may have. It is a simple chat application where users can ask about rules for different sports. Behind the hood is a RAG application using the Mistral-7B model for both embeddings and chat completion. 

## Running Locally

1) Install the necessary requirements with `pip install -r requirements.txt`
2) Move to the UI folder with `cd ui`
3) Run the streamlit app with `streamlit run SportsQA.py`