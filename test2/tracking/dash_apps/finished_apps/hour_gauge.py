import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('HourGauge', external_stylesheets=external_stylesheets)
my_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/insights/insights/most_active_hour.csv')
#val=my_data['Activation_count'].max()+my_data['Activation_count'].max()%10
hour=my_data[my_data['Activation_count']==my_data['Activation_count'].max()]['hour'].tolist()[0]
fig = go.Figure()
fig.add_trace(go.Indicator(
    mode = "gauge+number",
    value = hour,
    domain = {'x': [0, 1], 'y': [0, 1]},gauge = {'axis': {'range': [0 ,23]},'bar': {'color': "green"},'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "darkgreen"},
    )) 
#fig = px.line(my_data, x='hour', y='Activation_count')


fig.update_layout(
        font_family="Times New Roman",template="simple_white",paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font=dict(color='white',size=15),
       height=250
        
        )
fig.update_layout(margin={"r":15,"t":0,"l":15,"b":0,'pad':10})
app.layout = html.Div([
    
    
   dcc.Graph(figure=fig)
],style={})



    