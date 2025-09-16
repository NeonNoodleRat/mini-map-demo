from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    mapbox_access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
    return render_template("index.html", mapbox_access_token=mapbox_access_token)

if __name__ == "__main__":
    app.run(debug=True)