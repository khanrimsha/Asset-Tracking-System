import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('AvgDistance', external_stylesheets=external_stylesheets)

my_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/my_frame.csv')






    
x = []
for i in my_data['device']:
    x.append(i)

y = []
for i in my_data['latitude']:
    y.append(i)
fig=go.Figure()
fig.add_trace(go.Bar(
    x=x,
    y=y,
    name='Manipulate Graph',marker_color='#F7A705',opacity=0.8,marker_line_color='#F9D212',
    marker_line_width=1.5,
    ))
fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'autorange':True,'title':'Vehicle'},
        yaxis={'title':'Distance per day','autorange':True,'showgrid':False},
        font_family="Times New Roman",
        font=dict(color='white'),

    )
app.layout = html.Div([
   
    dcc.Graph(id='slider-graph',figure=fig, style={"backgroundColor": "black", }),
    
])