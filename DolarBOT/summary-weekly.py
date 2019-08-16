# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import tweepy, urllib, json, mysql.connector
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="aMTwTJCOPjPjJQcgIS7VPTJIG"
consumer_secret="8WQh12NTKbJfmWt2LuaojT8QXGEgBrA4v3fCCwHeXeN75ZXeiO"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1034524014478286849-aE0ax20mOESZ4XAxpiURH3e8gXxdTh"
access_token_secret="tXJL3TlIWi2KCoGfWtD4qwNpz7UeNo7tYiEEyxPLglFC2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
#print(api.me().name)

# If the application settings are set for "Read and Write" then

# API Core

# CONECTA LA BD
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "DolarBOT"
)

mycursor = mydb.cursor()

# SELECCIONA EL MAXIMO VALOR DE LA SEMANA
mycursor.execute("select date(date), max(rate) from rates WHERE date(date) BETWEEN DATE_SUB(NOW(), INTERVAL 6 DAY) AND NOW() group by date(date) order by max(rate) desc limit 1;")
result = mycursor.fetchall()

# SELECCIONA EL ULTIMO VALOR DE LA SEMANA PASADA
mycursor.execute("select date(date), max(rate) from rates WHERE date(date) BETWEEN DATE_SUB(NOW(), INTERVAL 14 DAY) AND DATE_SUB(NOW(), INTERVAL 6 DAY) group by date(date) order by date(date) desc limit 1;")
result2 = mycursor.fetchall()

items = []
for x in result:
	items.append({'date': x[0].strftime('%d/%m/%Y'), 'rate': x[1]})

items2 = []
for x in result2:
	items2.append({'date': x[0].strftime('%d/%m/%Y'), 'rate': x[1]})

variacion = ((items[0]['rate'] - items2[0]['rate']) / items2[0]['rate']) * 100

if variacion > 0:
	sign = "+"

	## Emoji pensativo
	emoji = u"\U0001F914"
	if variacion > 5:
		## Emoji cara al reves
		emoji = u"\U0001F643"
	
	if variacion > 10:
		## Emoji gritandoo
		emoji = u"\U0001F631"
else:
	sign = ""

	## Emoji lengua usd
	emoji = u"\U0001F911"

## Graph
emojiGraph = u"\U0001F4C8"
## Dolar
emojiDolar = u"\U0001F4B5"
## Dolar volando
emojiDolarVolando = u"\U0001F4B8"

mensaje = "El dólar esta semana llegó a $" + str(round(items[0]['rate'], 3)).replace(".", ",") + '\n('+sign+str(round(variacion, 2))+'%) respecto a la semana pasada. ' + emoji + ' \n\n#Dólar ' + emojiGraph + ' ' + emojiDolar + ' ' + emojiDolarVolando
#print(mensaje)

api.update_status(mensaje)
