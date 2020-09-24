import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SpeedGauge', external_stylesheets=external_stylesheets)
my_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')
#val=my_data['Activation_count'].max()+my_data['Activation_count'].max()%10
speed=my_data['SPEED'].max()
fig = go.Figure()
fig.add_trace(go.Indicator(
    mode = "gauge+number",
    value = speed,
    domain = {'x': [0, 1], 'y': [0, 1]},gauge = {'axis': {'range': [0 ,250]},'bar': {'color': "green"},'bgcolor': "black",
        'borderwidth': 2,
        'bordercolor': "darkgreen"},
    )) 
#fig = px.line(my_data, x='hour', y='Activation_count')


fig.update_layout(
        font_family="Times New Roman",
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font=dict(color='white',size=15),
        height=250,
        )
fig.update_layout(margin={"r":15,"t":0,"l":15,"b":0,'pad':10})
app.layout = html.Div([
   
   dcc.Graph(figure=fig)
])



    