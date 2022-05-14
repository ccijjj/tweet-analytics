from flask import Flask, render_template
import couchdb

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
    app.run()

try:
    couchclient = couchdb.Server('')
    tweet_db_name = ''
    
    #Check the duplication of database
    try:
        tweet_db = couchclient[tweet_db_name]
        print(tweet_db_name + " has already in the server!")
    except couchdb.http.ResourceNotFound:
        tweet_db = couchclient.create(tweet_db_name)
        print("Create " + tweet_db_name +" in the server!")
    print("Connected to the user database")
except:
    print("Cannot find CouchDB Server ... Exiting\n")
    print("----_Stack Trace_-----\n")
    raise