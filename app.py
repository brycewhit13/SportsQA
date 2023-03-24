#########################################################################
# Filename: app.py                                                      #
# Author: Bryce Whitney                                                 #
# Last Edit: 3/24/2023                                                  #
#                                                                       #
# Description: Runs the web application with the question and answering #
#########################################################################

# Imports
from flask import Flask, render_template, request
import sys
sys.path.append("scripts")
from scripts.question_answering import get_answer
from scripts.Sport import get_sport_from_str

# Initialize the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", qestion_display="", answer_display="")

@app.route("/result", methods=["GET"])
def result():
    question = request.args.get("question")    
    sport = get_sport_from_str(request.args.get("sport"))    
    answer = get_answer(question, sport)
    
    return render_template("index.html", question_display=question, answer_display=answer)