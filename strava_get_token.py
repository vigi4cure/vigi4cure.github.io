#!/usr/bin/python3

import requests
from stravalib.client import Client

client_id = 6389292
client_secret = '737adf5d50027f094540580034ca0e8b727c9568'

client = Client()
authorize_url = client.authorization_url(client_id=client_id, redirect_uri='http://localhost:8282/authorized')
# Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
# .....

# Extract the code from your webapp response
code = requests.get('code') # or whatever your framework does
access_token = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)

# Now store that access token somewhere (a database?)
client.access_token = access_token
athlete = client.get_athlete()
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))
