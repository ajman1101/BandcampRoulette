
from flask import Flask, url_for, request, redirect, render_template, session
app = Flask(__name__)

# Include the Dwolla REST Client
from dwolla import DwollaClientApp

# Include any required keys
import _keys

# Instantiate a new Dwolla User client
# And, Seed a previously generated access token
Dwolla = DwollaClientApp(_keys.apiKey, _keys.apiSecret)

'''
STEP 1: 
	Create an authentication URL
	that the user will be redirected to
'''
@app.route("/")
def index():
    oauth_return_url = url_for('dwolla_oauth_return', _external=True) # Point back to this file/URL
    permissions = 'Send'
    authUrl = Dwolla.init_oauth_url(oauth_return_url, permissions)
    return 'To begin the OAuth process, send the user off to <a href="%s">%s</a>' % (authUrl, authUrl)
'''
STEP 2: 
	Exchange the temporary code given
	to us in the querystring, for
	a never-expiring OAuth access token
'''

@app.route("/dwolla/oauth_return")
def dwolla_oauth_return():
    oauth_return_url = url_for('dwolla_oauth_return', _external=True) # Point back to this file/URL
    code = request.args.get("code")
    token = Dwolla.get_oauth_token(code, redirect_uri=oauth_return_url)
    return 'Your never-expiring OAuth access token is: <b>%s</b>' % token

# Run the app
if __name__ == "__main__":
	app.run(debug=True)
