import json
from flask import Flask, render_template
from artifact.database import init_db

app = Flask(__name__, template_folder="../templates")
init_db()

@app.route("/")
def index():
    return render_template("index.html")