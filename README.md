# Sports Rule Clarification

## Problem

In the most popular sports leagues (NFL, NHL, FIFA, etc.) there can be hundreds of pages in the rulebook
that players, coaches, and referees are expected to follow. The average fan doesn’t read or remember
the entire rulebook and if they have a question about the rules, they need to parse through hundreds of
pages to find an answer. These pages are dense and contain lots of jargon as they are designed to cover
every situation that may happen in a game. This lawyer-like precision adds a lot of information that is
simply unnecessary for 95% of fans. On top of this, the rules are constantly updating each year and it can
be very difficult to keep track of everything.

## Goal

The goal of this project is to create a web application where people can go and have all their questions about the current rules in sports answered. Through interacting with a chatbot, users can ask any questions about the rules and they will get a response that summarizes what the rule is and how it is enforced. The goal is to have a simple response that gives the main points without all the jargon from the rulebook.

Support is currently available for the current sports and leagues:

- American Football (NFL)
- Hockey (NHL)
- Men's Basketball (NBA)
- Women's Basketball (WNBA)
- Ultimate (USAU)

## Data

For each sport that is currently supported, the most recent official rulebooks were either downloaded from the web in pdf form or scraped directly from a league website. You can find the official rules for each sport linked below:

- [American Football (NFL)](https://operations.nfl.com/media/5kvgzyss/2022-nfl-rulebook-final.pdf)
- [Hockey (NHL)](https://cms.nhl.bamgrid.com/images/assets/binary/335473802/binary-file/file.pdf)
- [Men's Basketball (NBA)](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2022/10/Official-Playing-Rules-2022-23-NBA-Season.pdf)
- [Women's Basketball (WNBA)](https://www.wnba.com/wnba-rule-book/)
- [Ultimate (USAU)](https://www.usaultimate.org/about/rules/)

Minimal preprocessing was done on the data since the word and sentence structure is important for understanding meaning in the Q&A context. All the data was converted to text files and converted to completely lowercase letters before modeling.

## Approach

### TF-IDF

The first approach was to create sentence embeddings for each of the rulebooks using [TF-IDF](https://monkeylearn.com/blog/what-is-tf-idf/) embeddings. An question embedding would also be created using TF-IDF, and then each sentence in the rulebook is compared with the question to determine which sentence has the highest cosine similarity. This sentence is returned as the answer to the question.

This approach oftentimes picked out sentences related to the main topic of the question, but it was unable to distinguish when the topic is being defined or if it is being used in a context in which something else is being described. This approach got **0 / 59** of the questions correct in the validations set.

### FAISS Document Search

[FAISS](https://github.com/facebookresearch/faiss) stands for Facebook AI Similarity Search and is a technique to search large documents very quickly without sacrificing much performance. This works by chunking larger documents into smaller documents and creating embeddings within each of those to create a database called a [document store](https://docs.haystack.deepset.ai/docs/document_store). I implemented this using the python [Haystack](https://haystack.deepset.ai/) Module.

I decided to use an extractive approach over a generative summary approach here for a couple reasons:

1. It generates an answer more efficiently
2. The rules are very precise, and generating summaries on them does have the risk of losing some of the nuance for certain rules.

This approach was able to answer some questions correctly, but also got a lot wrong. It seems to struggle with numbers in particular, and getting confused on the context each number is associated with. However, it does have the added benefit of being easily explainable because we can see exactly where the model got it's answer from in the rulebook. This approach was able to answer **20 / 59** questions correct from the validation set.

### GPT 3.5

Finally I experimented with using OpenAI's GPT-3.5 model to answer questions. Originally I did not provide the model any context about the rules, and it was able to answer **52 / 59** questions correct. A massive improvement! To try and improve this, I created generative summaries for each rulebook that can be passed as context to the model. These summaries are around 2000-2500 words each because I wanted to keep it to a single query when using the GPT-3.5 model. This additional context was able to improve the results and correctly answered **55/59** questions from the validation set. This is the approach implemented in the flask application.

## Running the App

### Locally

To run the app locally, follow the steps below:

1. Ensure you have [OPENAI API Key](https://platform.openai.com/account/api-keys). You may need to create an account to generate one if you don't have an account already. Once you have generated a key, save it to your environment variables with the `name` as `OPENAI_API_KEY` and the `value` as the key.
    - **NOTE**: There is a minor charge of about 1 cent for every question that is asked, so beware of this if you are using your own API key.  
2. Install all the requirements with `pip install -r requirements.txt`

3. Run the command `flask run` and go to [](https://127.0.0.1:5000/). After that, you should be able to use the app without any issues.

### Online

 You can test out the application online [here](http://sports-rules-clarifications.azurewebsites.net/)
