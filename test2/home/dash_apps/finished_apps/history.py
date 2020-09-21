import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import folium
from branca.element import Figure
import plotly.express as px
import json
import dash_table
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('history', external_stylesheets=external_stylesheets)

geo_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


app.layout = html.Div([
 
       
        html.Div([
            dash_table.DataTable(id='table',
            
    columns=[{'id': c, 'name': c} for c in ['DATE','TIME','LATITUDE','LONGITUDE','SPEED']] ,
    data=geo_data.to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_cell_conditional=[
        {
            
            'textAlign': 'left',
            'backgroundColor': 'rgb(255,255,255)',
        'color': 'black'
        }],
    style_as_list_view=True,
    style_header={'backgroundColor': '#add8e6','color': 'black'},
    
)
        ])
        ])




    


