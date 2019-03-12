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
consumer_key="WeD9aMdBeN2O0HjQrwd7ksG49"
consumer_secret="l7qPb3aNZ56F9A2yagoNTGkjLKdQdkMwqzipQ4apXaHcxm8dDp"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1105599460992786433-XMTwRAEYTEwvCWAsAqDKVcOo0eqMNL"
access_token_secret="M8Fbj2sc8Lcw8hhv0FKyvmQq5Df5ZUx2KsPuqHDpKno4n"

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
	database = "anda_a_bot_bobo"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS tweets (id INT AUTO_INCREMENT PRIMARY KEY, tweet VARCHAR(50), tweeted_at DATETIME, link VARCHAR(150));")

mycursor.execute("SELECT articulo, palabra FROM palabras ORDER BY RAND() LIMIT 1;")

result = mycursor.fetchall()

frase = []

for a in result:
    frase.append({'articulo': a[0], 'palabra': a[1]})


tweet = "andá a " + str(frase[0]['articulo']) + ' ' + str(frase[0]['palabra']) + " bobo."

print(tweet)

try:
    api.update_status(status=tweet)

    sql = "INSERT INTO tweets (tweet) VALUES (%s);"
    val = (tweet)
    mycursor.execute(sql, val)
    mydb.commit()
except:
    sql = "INSERT INTO tweets (tweet) VALUES (%s);"
    val = ("No se pudo twittear :(")
    mycursor.execute(sql, val)
    mydb.commit()


