from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def home():
    """
    render homepage of webapp
    """
    #GET REAL VALUES
    attention_counter = 0
    attention_avrg = 0
    return render_template('index.html',
                           attention_counter=attention_counter,
                           attention_avrg=attention_avrg)

