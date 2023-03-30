#########################################################################
# Filename: app.py                                                      #
# Author: Bryce Whitney                                                 #
# Last Edit: 3/24/2023                                                  #
#                                                                       #
# Description: Runs the web application with the question and answering #
#########################################################################

# Imports
import os
from flask import Flask, render_template, request
import sys
sys.path.append("scripts")
from scripts.question_answering import get_answer
from scripts.Sport import get_sport_from_str

# Initialize the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", qestion_display="", answer_display="")

@app.route("/result", methods=["GET"])
def result():
    question = request.args.get("question")    
    sport = get_sport_from_str(request.args.get("sport"))   
    answer, context = get_answer(question, sport)

    print(f"\nQuestion: {question}")
    print(f"Answer: {answer}")
    print(f"Context: {context}\n")
    
    return render_template("index.html", question_display=question, answer_display=answer)