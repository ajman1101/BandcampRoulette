from flask import Flask, url_for, redirect, render_template, request, session
import scrape

from dwolla import DwollaClientApp, DwollaUser

Dwolla = DwollaClientApp("Q/9GH5LwLTp06+VUj7Rt9iKFgyIOQmFZF0AxTEAYyWoC84P4YN", "ePRDZwcOOTjPbZ5rdyRvZpg6GMpHrUyxyQLNQzowFMiUtov2g")

app = Flask(__name__)
app.secret_key = "key"


@app.route('/')
def index():
    oauth_return_url = url_for('dwolla_oauth_return', _external=True)#point back to this file
    permissions = 'send'
    auth_url = Dwolla.init_oauth_url(oauth_return_url, permissions)
    url = None
    title = None
    if request.args.get("search"):
        try:
            url, title = scrape.scrape(request.args.get("search"))
        except TypeError as e:
            url = "No song found"
            title = None

    return render_template("index.html", song=url, title=title, auth_url=auth_url)


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


@app.route('/finish')
def finish_songs():
    if not session['done']:
        session['done'] = True
    else:
        del session['done']
        session['liked_songs'] = dict()
    redirect(url_for('index'))


#STEP:2 = temp code exchange
@app.route("/dwolla/oauth_return")
def dwolla_oauth_return():
    oauth_return_url = url_for('dwolla_oauth_return', external=True)#print back to this file/URL
    code = request.args.get("code")
    token = Dwolla.get_oauth_token(code, redirect_uri=oauth_return_url)
    session['token'] = token
    return 'Your never-expiering OAuth access token is: <b>%s</b>' % token


#STEP 3: Take Token and swap it into the right place
@app.route("/dwolla/donate")
def donate():
    user = DwollaUser(session['token'])
    transactionId = user.send_funds(0.00, 'phone #', '[PIN]')
    print transactionId

if __name__ == '__main__':
    app.debug = True
    app.run()
