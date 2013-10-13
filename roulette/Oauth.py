#include flask
from flask import Flask, url_for, request, redirect, render_template, session
app = Flask(__name__)

#include the Dwolla REST client
from dwolla import DwollaClientApp

#pull in memcached to store the token for a bit
from memcache import Client

#sets up connection on local machine on the port 1121
cache = Client(['127.0.0.1:11211'])

#dates and times for user hash
from datetime import datetime

#gets hash stuff
from hashlib import md5

#import required keys
#import _keys

#hard coded the (api.Key,api.Secret)
Dwolla = DwollaClientApp("Q/9GH5LwLTp06+VUj7Rt9iKFgyIOQmFZF0AxTEAYyWoC84P4YN", "ePRDZwcOOTjPbZ5rdyRvZpg6GMpHrUyxyQLNQzowFMiUtov2g")

#STEP 1:
#Create an authentication URL that the user will be redirected to

@app.route("/")
def index():
    oauth_return_url = url_for('dwolla_oauth_return', _external=True)#point back to this file
    permissions = 'send'
    authUrl = Dwolla.init_oauth_url(oauth_return_url, permissions)
    m = md5()
    m.update(request.headers.get('user-agent') + str(datetime.now))
    session ['userId'] = m.hexdigest()
    return 'To begin the OAuth process, send the user off to <a href"%s">%s</a>' % (authUrl, authUrl)

#STEP 2:
#Exchange the temp code given to use in the querystring , for a never expiring OAuth access token

@app.route("/dwolla/oauth_return")
def dwolla_oauth_return():
    oauth_return_url = url_for('dwolla_oauth_return', external=True)#print back to this file/URL
    code = request.args.get("code")
    token = Dwolla.get_oauth_token(code, redirect_uri=oauth_return_url)
    cache.set(session['userId'], token)
    print session['userId'], token
    return 'Your never-expiering OAuth access token is: <b>%s</b>' % token


#STEP 3: Take Token and swap it into the right place
@app.route("/dwolla/donate")
def donate():
    token = cache.get(session['userId'])
    DwollaUser = DwollaUser(token)
    transactionId = DwollaUser.send_funds(0.00, 'phone #', '[PIN]')
    print transactionId




#Run the App
if __name__ == "__main__":
    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
