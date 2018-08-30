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
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
#api.update_status(status='Updating using OAuth authentication via Tweepy!')

# API Core

key      = "7dcae92e858e039cbaa9c3f2b58d49c3"
url      = "http://data.fixer.io/api/latest?access_key="+key+"&symbols=ARS,USD"
response = urllib.urlopen(url)
data     = json.loads(response.read())

ARS       = data['rates']['ARS']
USD       = data['rates']['USD']
timestamp = data['timestamp']
date      = datetime.utcfromtimestamp(timestamp) - timedelta(hours=3) 

dateFormat = date.strftime('%H:%M %d/%m/%Y')

rate =  ARS / USD

print(round(rate, 4))

# GUARDA EN LA BD
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "DolarBOT"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS rates (id INT AUTO_INCREMENT PRIMARY KEY, date DATETIME, rate FLOAT)")

sql = "INSERT INTO rates (date, rate) VALUES (%s, %s)"
val = (date, rate)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

# COMPARA EL ULTIMO TWEET CON EL ANTERIOR PARA VER SI SUBIO O NO
mycursor.execute("select date, rate from rates order by id desc limit 2")
result2 = mycursor.fetchall()

items2 = []
for y in result2:
        items2.append({'date': y[0], 'rate': y[1]})

if items2[0]['rate'] < items2[1]['rate']:
        subio = "No"
else:
        subio = "Sí"

# SELECCIONA EL ULTIMO VALOR DE CADA DIA PARA HACER LA VARIACION PORCENTUAL
mycursor.execute("select date, rate from rates inner join ( select max(date) as max from rates group by date(date) ) rates2 on rates.date = rates2.max order by date desc;")
result = mycursor.fetchall()

items = []
for x in result:
	items.append({'date': x[0], 'rate': x[1]})

if items[0]['rate'] < items[1]['rate']:
	print("La de hoy es menor que la de ayer")
else:
	print("La de hoy es mayor que la de ayer")

variacion = ((items[0]['rate'] - items[1]['rate']) / items[1]['rate']) * 100

#print(variacion)
#print(items)

api.update_status(status=subio+' desde el último Tweet, ahora está $'+str(round(rate, 4))+'. \nVarió '+str(round(variacion, 2))+'% con respecto al cierre de ayer. \n\n(Actualizado: '+dateFormat+')')

