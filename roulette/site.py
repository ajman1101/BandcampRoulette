import os

from flask import Flask, url_for, redirect, render_template, request, session
import scrape

#from dwolla import DwollaClientApp, DwollaUser

#Dwolla = DwollaClientApp(
#    "Q/9GH5LwLTp06+VUj7Rt9iKFgyIOQmFZF0AxTEAYyWoC84P4YN",
#    "ePRDZwcOOTjPbZ5rdyRvZpg6GMpHrUyxyQLNQzowFMiUtov2g")

app = Flask(__name__)
app.secret_key = "key"

base_path = os.path.split(__name__)[0]


@app.route('/')
def index():
#    oauth_return_url = url_for('dwolla_oauth_return',
#                               _external=True)  # point back to this file
#    permissions = 'send'
    auth_url = ''  # Dwolla.init_oauth_url(oauth_return_url, permissions)
    search = None
    if request.args.get('random'):
        with open(os.path.join(base_path, 'static', 'words.txt')) as wordfile:
            import random
            line = random.choice(wordfile.readlines())
        search = line

    elif request.args.get("search"):
        search = request.args['search']

    try:
        url, title = scrape.scrape(search)
    except TypeError:
        url = "No song found"
        title = None

    return render_template("index.html", search=search, song=url, title=title,
                           auth_url=auth_url)


@app.route('/like', methods=['POST'])
def addSong():
    url = request.form.get("url")
    title = request.form.get("title")
    if url and title:
        if not session.get('liked_songs'):
            session['liked_songs'] = {}
        if session['liked_songs'].get(url):
            # No need to send a respone, it's already been seen
            return '', 204
        session['liked_songs'][url] = title
    return u"<a href='{}' target='_blank'>{}</a>".format(url, title)


@app.route('/results')
def show_results():
    #winner= request.args.get('winner')
    song = request.args.get('song')
    return render_template('winner.html', user=None, song_url=song)


@app.route('/finish')
def finish_songs():
    if not session.get('done'):
        session['done'] = True
    else:
        del session['done']
        session['liked_songs'] = dict()
    return redirect(url_for('index'))


#STEP:2 = temp code exchange
#@app.route("/dwolla/oauth_return")
#def dwolla_oauth_return():
#    oauth_return_url = url_for(
#        'dwolla_oauth_return', external=True)#print back to this file/URL
#    code = request.args.get("code")
#    token = Dwolla.get_oauth_token(code, redirect_uri=oauth_return_url)
#    session['token'] = token
#    return 'Your never-expiering OAuth access token is: <b>%s</b>'  # % token


#STEP 3: Take Token and swap it into the right place
#@app.route("/dwolla/donate")
#def donate():
#    user = DwollaUser(session['token'])
#    transactionId = user.send_funds(0.00, 'phone #', '[PIN]')
#    print transactionId

if __name__ == '__main__':
    app.debug = True
    app.run()
