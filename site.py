from flask import Flask, render_template, request
import scrape


app = Flask(__name__)


@app.route('/')
def bandcampRoulette():

    info = [None]
    if request.args.get("search"):
        info = scrape.scrape(request.args.get("search"))
    return render_template("index.html", song=info[0])

if __name__ == '__main__':
    app.debug = True
    app.run()
