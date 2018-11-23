# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta
from plotly.graph_objs import *

import tweepy, urllib, json, mysql.connector, plotly.plotly as py, pandas as pd, locale, os, numpy as np
import plotly.io as pio

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

if not os.path.exists('images'):
    os.mkdir('images')

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
    title='Seguimiento del precio del dólar durante el mes de '+str(datetime.now().strftime('%B')),
    xaxis=XAxis( type='date', title='Día' ),
    yaxis=YAxis( title='Valor ($ ARS)', automargin=True, range=[30, 42] ),
    height=500,
    width=850
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)

pio.write_image(fig, 'images/Monthly Graph - Mes: '+str(datetime.now().strftime('%m'))+'.png')
#py.iplot(fig, filename='Monthly Graph - Mes: '+str(datetime.now().strftime('%m')))

mensaje = 'Imagen guardada: "images/Monthly Graph - Mes: '+str(datetime.now().strftime('%m'))+'.png"'

#api.update_status(mensaje)
api.update_with_media('images/Monthly Graph - Mes: '+str(datetime.now().strftime('%m'))+'.png', '¡Mirá el resúmen mensual de la evolución del precio del dólar!')
#print(mensaje)
