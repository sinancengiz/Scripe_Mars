# import necessary libraries
from flask import Flask, render_template, redirect
import scripe_file
import pandas as pd

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

#app route to scrape
@app.route('/scripe_data')
def scrape_data():
    data = scripe_file.scripe_func()
    return render_template("scripe.html", mars=data)

#Run the app. debug=True is essential to be able to rerun the server any time changes are saved to the Python file
if __name__ == "__main__":
    app.run(debug=True, port=5000)