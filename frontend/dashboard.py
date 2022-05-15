from flask import Flask, render_template
import couchdb
import sys

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/dash")
def dash():
    return render_template('dashboard.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/language")
def language():
    return render_template('language.html')
@app.route("/rent")
def rent():
    return render_template('rent.html')
@app.route("/env")
def env():
    return render_template('environment.html')
@app.route("/unem")
def unem():
    return render_template('unemployment.html')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Please provide the correct Couch DB information")
        print("Usage: python3 dashboard.py <usr> <pwd> <ip> <db name>")
        sys.exit(1)
    
    usr, pwd, ip, tweet_db_name = sys.argv[1:5]
    try:
        couchclient = couchdb.Server(f"http://{usr}:{pwd}@{ip}:5984/")
        tweet_db = couchclient[tweet_db_name]
    except:
        print("Cannot find CouchDB Server ... Exiting\n")
        print("----_Stack Trace_-----\n")
        raise
    
    app.run()
