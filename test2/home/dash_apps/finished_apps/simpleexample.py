import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import math 
from firebase import firebase
import folium

database=firebase.FirebaseApplication("https://assetdata-5e192.firebaseio.com/",None)
data=database.get('/assetdata-5e192/car/KI7MH-7/insights/average_hour_week/','')
my_data=pd.DataFrame(data)

# external JavaScript files
external_scripts = [
    'https://unpkg.com/leaflet@1.0.3/dist/leaflet.js',
    {'src': 'C:/Users/Rimsha khan/Desktop/leaflet.js'},
    
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'C:/Users/Rimsha khan/Desktop/mycss.css',
        'rel': 'stylesheet',
       
    }
    ,
    {
        'href': ' https://unpkg.com/leaflet@1.0.3/dist/leaflet.css',
        'rel': 'stylesheet',
    }
]
app = DjangoDash('SimpleExample', external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

geo_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')

geo_data=geo_data.dropna(subset=['LATITUDE','LONGITUDE'])
my_data=geo_data[geo_data['DATE']=='2020-06-07']
listt=my_data.loc[:,['LATITUDE','LONGITUDE']].values.tolist()
last_co_ords=my_data.loc[:,['LATITUDE','LONGITUDE']].tail(1).values.tolist()
m2=folium.Map(height=500,location=listt[0],zoom_start=6,tiles='cartodbpositron',attr='by Rimsha Khan')

folium.vector_layers.PolyLine(listt,popup='<b>Path of Vehicle</b>',tooltip='Track of 2020-06-07',color='blue',weight=3).add_to(m2)

folium.Marker(location=listt[0],popup='Starting Point',tooltip='<strong>Starting Point</strong>',icon=folium.Icon(color='red',prefix='fa',icon='anchor')).add_to(m2)
folium.Marker(className='blinking',location=last_co_ords[0],popup='Finish Point',tooltip='<strong>Finish Point</strong>',icon=folium.features.CustomIcon('https://unpkg.com/leaflet@1.0.3/dist/images/marker-icon.png')).add_to(m2)

m2.save('C:/Users/Rimsha khan/Desktop/map.html')


app.layout = html.Div(id='map')





  
    
    
    
    
    