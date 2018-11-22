# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta
from plotly.graph_objs import *

import tweepy, urllib, json, mysql.connector, plotly.plotly as py, pandas as pd, locale

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

# TOKEN PLOTLY
py.sign_in('ezebrotsky', 'mwFQHToLhWjR6tWF0y9A')

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

# SELECCIONA EL VALOR MÁXIMO DE CADA DÍA DEL MES
mycursor.execute("select date(date), max(rate) from rates WHERE date(date) BETWEEN LAST_DAY(NOW() - INTERVAL 1 MONTH) + INTERVAL 1 DAY AND NOW() group by date(date) order by date(date);")
result = mycursor.fetchall()

locale.setlocale(locale.LC_TIME, 'es_AR.utf8')

df = pd.DataFrame( [[ij for ij in i] for i in result] )
df.rename(columns={0: 'Date', 1: 'Rate'}, inplace=True);

df.head()

trace1 = Scatter(
    x=pd.to_datetime(df['Date']),
    y=df['Rate'],
    mode='lines+markers',
	line=dict(
		shape='linear'
	    )
)
layout = Layout(
    title='Variación de '+str(datetime.now().strftime('%B')),
    xaxis=XAxis( type='date', title='Día' ),
    yaxis=YAxis( title='Valor', automargin=True ),
    height=500,
    width=850
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='Monthly Graph - Mes: '+str(datetime.now().strftime('%m')))

mensaje = ""

#api.update_status(mensaje)
