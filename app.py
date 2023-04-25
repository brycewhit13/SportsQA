#########################################################################
# Filename: app.py                                                      #
# Author: Bryce Whitney                                                 #
# Last Edit: 4/24/2023                                                  #
#                                                                       #
# Description: Runs the web application with the question and answering #
#########################################################################

##### Imports #####
from flask import Flask, render_template, request
import sys
sys.path.append("scripts")

from scripts.question_answering import gpt_answer_with_context
from scripts.Sport import get_sport_from_str, get_league, get_official_rulebook

#############################
##### App Functionality #####
#############################

# Initialize the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Starting page
@app.route("/")
def index():
    return render_template("index.html", question_display="", answer_display="", nfl_checked="checked")

@app.route("/result", methods=["GET"])
def result():
    # Extract the sport and question from the request
    question = request.args.get("question")
    sport = get_sport_from_str(request.args.get("radio"))
    
    # Get the answer to the question and return the result
    answer = gpt_answer_with_context(question, sport)
    
    # Get the link to the official rulebook
    more_info_text = "If you want to explore the rules yourself, you can "
    link_text = "visit the official rulebook here."
    link = get_official_rulebook(sport)
    
    # Determine which radio button should be checked
    league = get_league(sport, lower=True)
    if(league == "nfl"):
        return render_template("index.html", question_display=question, answer_display=answer, nfl_checked="checked", link_text=link_text, link=link, more_info_text=more_info_text)
    elif(league == "nhl"):
        return render_template("index.html", question_display=question, answer_display=answer, nhl_checked="checked", link_text=link_text, link=link, more_info_text=more_info_text)
    elif(league == "nba"):
        return render_template("index.html", question_display=question, answer_display=answer, nba_checked="checked", link_text=link_text, link=link, more_info_text=more_info_text)
    elif(league == "wnba"):
        return render_template("index.html", question_display=question, answer_display=answer, wnba_checked="checked", link_text=link_text, link=link, more_info_text=more_info_text)
    else:
        return render_template("index.html", question_display=question, answer_display=answer, usau_checked="checked", link_text=link_text, link=link, more_info_text=more_info_text)
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)