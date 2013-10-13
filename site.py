from flask import Flask, render_template, request
import scrape


app = Flask(__name__)


@app.route('/')
def bandcampRoulette():

    song = None
    if request.args.get("search"):
        song = scrape.scrape(request.args.get("search"))
    return render_template("index.html", song=song)

if __name__ == '__main__':
    app.debug = True
    app.run()
