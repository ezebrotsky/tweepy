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

items = []
for x in result:
	items.append({'date': x[0].strftime('%d/%m/%Y'), 'rate': x[1]})

# SELECCIONA EL MINIMO VALOR DE LA SEMANA
mycursor.execute("select date(date), max(rate) from rates WHERE date(date) BETWEEN DATE_SUB(NOW(), INTERVAL 6 DAY) AND NOW() group by date(date) order by max(rate) limit 1;")
result2 = mycursor.fetchall()

items2 = []
for y in result2:
	items2.append({'date': y[0].strftime('%d/%m/%Y'), 'rate': y[1]})

mensaje = "Resumen de la semana: \nEl valor máximo que tomó el dólar fue de $" + str(round(items[0]['rate'], 3)).replace(".", ",") + " el " + items[0]['date'] + ".\nMientras que el mínimo fue de $" + str(round(items2[0]['rate'], 3)).replace(".", ",") + " el " + items2[0]['date'] + "."
#print(mensaje)

api.update_status(mensaje)
