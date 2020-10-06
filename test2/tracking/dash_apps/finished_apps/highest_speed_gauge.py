import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px
from tracking import functions
session_val=None


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SpeedGauge', external_stylesheets=external_stylesheets)


app.layout = html.Div([
   dcc.RadioItems(
                id="Month",
               
                value='Weekly',
                
                style={'color':'white'},
                ),
   dcc.Graph(id="gauge")
])
@app.expanded_callback(
            Output('gauge', 'figure'),
            [Input('Month', 'value')])
def display_value(value,**kwargs):
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
 
    speed=functions.fetch_insight(type_,dev,'peak_speed')
  
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = speed,
        number= dict( suffix= "<br>km/hr" ),
        domain = {'x': [0, 1], 'y': [0, 1]},gauge = {'axis': {'range': [0 ,250]},'bar': {'color': "green"},'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "darkgreen"},
        )) 
    


    fig.update_layout(
            font_family="Times New Roman",
            paper_bgcolor='rgba(0,0,0)',
            plot_bgcolor='rgb(0,0,0)',
            font=dict(color='white',size=15),
            height=250,
            )
    fig.update_layout(margin={"r":15,"t":0,"l":15,"b":0,'pad':10})
    return fig




    