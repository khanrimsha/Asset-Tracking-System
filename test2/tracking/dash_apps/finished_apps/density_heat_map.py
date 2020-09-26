import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('HeatMap', external_stylesheets=external_stylesheets, )
my_data=pd.read_json('C:/Users/Rimsha khan/Desktop/insights/insights/aircrafts.json'
                   )
fig = go.Figure(go.Densitymapbox(lat=my_data.Lat, lon=my_data.Long, z=my_data.Alt,
                                 radius=10,hovertemplate =
    '<b>Co-ordinates:( %{lat}'+' %{lon}) </b>'+'<b> Altitude</b>: %{z}'+
        "<extra></extra>"))
fig.update_layout(mapbox_style="carto-darkmatter", mapbox_center_lon=180)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 



fig.update_layout(
       
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font=dict(color='white'),
        )

app.layout = html.Div([
  
   dcc.Graph(figure=fig)
])



    