from flask import Flask, render_template, request, session
import scrape


app = Flask(__name__)
app.secret_key = "key"


@app.route('/')
def bandcampRoulette():

    url = None
    title = None
    if request.args.get("search"):
        try:
            url, title = scrape.scrape(request.args.get("search"))
            if not session.get('all_songs'):
                session['all_songs'] = {}
                session['liked_songs'] = {}
            session['all_songs'][url] = title
        except TypeError as e:
            print(e)
            pass

    return render_template("index.html", song=url, title=title)


@app.route('/like')
def addSong():

    if request.args.get("url") and request.args.get("title"):
        url = request.args["url"]
        title = request.args["title"]
        if not session.get('liked_songs'):
            session['liked_songs'] = {}
        session['liked_songs'][url] = title
        return "Song added"
    return "Song not added"

if __name__ == '__main__':
    app.debug = True
    app.run()
