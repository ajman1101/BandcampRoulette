from flask import Flask, render_template, request, session
import scrape


app = Flask(__name__)
app.secret_key = "key"


@app.route('/')
def bandcampRoulette():

    info = None
    if request.args.get("search"):
        info = scrape.scrape(request.args.get("search"))
        if info is not None:
            session['songs'] = [info[0], info[1]]
            print(session['songs'])
            return render_template("index.html", song=info[0], session=session)
    return render_template("index.html", song=info)

if __name__ == '__main__':
    app.debug = True
    app.run()
