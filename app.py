from flask import Flask, render_template, send_from_directory
# from pymongo import MongoClient
import os

app = Flask(__name__)
SHARED_IMGS = "/shared/img"

@app.route("/")
def home():
    """
    render homepage of webapp
    """
    #GET REAL VALUES
    # attention_avrg = 0
    time_attn_lost = "time attention was lost"
    images = os.listdir(SHARED_IMGS)
    attention_counter = len(images)
    return render_template('index.html',
                           attention_counter=attention_counter,
                        #    attention_avrg=attention_avrg,
                           time_attn_lost=time_attn_lost,
                           images=images)

@app.route("/images/<filename>")
def get_image(filename):
    return send_from_directory(SHARED_IMGS, filename)

app.run(host="0.0.0.0", port=5000)