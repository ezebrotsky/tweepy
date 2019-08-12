# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import tweepy, urllib, json, mysql.connector

import requests
from bs4 import BeautifulSoup

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

## Tomo valor de dolarhoy.
r = requests.get('http://dolarhoy.com/')

soup = BeautifulSoup(r.text, "html.parser")

now = datetime.now()

date = now
unformatedRate = soup.findAll('span')[2].get_text()

unformatedRate = unformatedRate.replace("$ ", "")
rate = float(unformatedRate.replace(",", "."))

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

if round(items2[0]['rate'], 3) <= round(items2[1]['rate'], 3):
        subio = "No"
	mensaje = "No, desde el último Tweet bajó a"
	
	if round(items2[0]['rate'], 3) == round(items2[1]['rate'], 3):
		mensaje = "No, desde el último Tweet se mantuvo en"
else:
        subio = "Sí"
	mensaje = "Sí, desde el último Tweet subió a"

# SELECCIONA EL ULTIMO VALOR DE CADA DIA PARA HACER LA VARIACION PORCENTUAL
mycursor.execute("select date, rate from rates inner join ( select max(date) as max from rates group by date(date) ) rates2 on rates.date = rates2.max order by date desc;")
result = mycursor.fetchall()

items = []
for x in result:
	items.append({'date': x[0], 'rate': x[1]})

variacion = ((round(items[0]['rate'], 3) - round(items[1]['rate'], 3)) / round(items[1]['rate'], 3)) * 100

if variacion > 0:
	sign = "+"
else:
	sign = ""

status = 'Valor actual: $'+str(round(rate, 3)).replace(".", ",")+'. \n('+sign+str(round(variacion, 2))+'%) respecto al día de ayer. \n\n#Dólar'

api.update_status(status=status)
#print(status)

