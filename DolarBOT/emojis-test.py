# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import tweepy, urllib, json, mysql.connector

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="bUxH0cgHZNEaVVYkWnSwRGEat"
consumer_secret="SDjn7TCSEn1RgGmnl5GSYkPqbCx75r0tIglrtqya79KzitgyjV"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="762291883-o6jZ4kAmT6lC33qJxKZiMddppAKlZSgKmsyiH0NH"
access_token_secret="prxVwl5XasAPwWtyshd450peSSybZdDv76W3sSvBqGmQR"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
#print(api.me().name)

# If the application settings are set for "Read and Write" then

# API Core

#mensaje = "Valor máximo de hoy: $"+str(round(items[0]['rate'], 3)).replace(".", ",")+". \n\n#Dólar"
#print(mensaje)

## Emoji pensativo
emoji1 = u"\U0001F914"
## Emoji cara al reves
emoji2 = u"\U0001F643"
## Emoji lengua usd
emoji3 = u"\U0001F911"
## Graph
emoji4 = u"\U0001F4C8"
## Dolar
emoji5 = u"\U0001F4B5"
## Dolar volando
emoji6 = u"\U0001F4B8"

mensaje = emoji1 + " " + emoji2 + " " + emoji3 + " " + emoji4 + " " + emoji5 + " " + emoji6

api.update_status(mensaje)
