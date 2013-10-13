from flask import Flask, render_template, request, session
import scrape


app = Flask(__name__)
app.secret_key = "key"


@app.route('/')
def bandcampRoulette():

    url = None
    if request.args.get("search"):
        try:
            url, title = scrape.scrape(request.args.get("search"))
            if not session.get('songs'):
                session['songs'] = {}
            session['songs'][url] = title
        except TypeError as e:
            print(e)
            pass

    return render_template("index.html", song=url)

if __name__ == '__main__':
    app.debug = True
    app.run()
