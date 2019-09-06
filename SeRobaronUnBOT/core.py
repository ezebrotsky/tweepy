# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import tweepy, json, mysql.connector

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="xvslmEL2w6mja0BTX5ktIBroG"
consumer_secret="2sLVx2FkRMjFOVGbkEYVfLIy3iJP4x85iox54I9k34jvl9etdL"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1169762380051562502-zyoikZTtFeKXeX8dDxokuMHhofh2H3"
access_token_secret="ANENsTh8LLXMpmwLzIEqVY1ag4JL0hm24VP6ztyjqWZjj"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
#print(api.me().name)

# If the application settings are set for "Read and Write" then

# API Core

# GUARDA EN LA BD
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "SeRobaronUnBOT"
)

mycursor = mydb.cursor()

# SELECCIONA UN ACRONIMO QUE NO HAYA SIDO LEIDO
mycursor.execute("select acronimo, id from acronimos where leido = 0 order by id asc limit 1")
result = mycursor.fetchall()

status = ""

if result:
	for x in result:
		status = 'Se robaron un ' + x[0]
		mycursor.execute("UPDATE acronimos SET leido = 1 WHERE id = " + str(x[1]))
		mydb.commit()
else:
	print("No hay mas acronimos")

if status != "":
	api.update_status(status=status)
print(status)
