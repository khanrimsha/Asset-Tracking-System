import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
try:
    cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
    firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
except:
    pass
database=db.reference("car/KC7LZD-9/insights/most_active_time_duration_week/")
d=database.get()
data_json = json.loads(d)
my_data=pd.DataFrame(data_json)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('AvgActiveHourWeek', external_stylesheets=external_stylesheets)
week=my_data['x']
val=my_data['y']

fig=go.Figure()
for i in range(0,len(week)):
        fig.add_trace(go.Bar(x = [week[i]],
                        y =[val[i]],
                        marker_line_color='#F9D212',
                        
                        marker_color='#F9D212',
                        opacity=0.5,
                        hovertemplate =
    '<b>Day</b>: %{x}  '+'<b>Active Hours</b>: %{y}'+
        "<extra></extra>"
    
    ,
                        
                        
        ))
fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'title':'Days','autorange':True,'showgrid':False,'fixedrange':True},
        yaxis = dict(title='Active Hours',showgrid=False,fixedrange=True),
        
        font=dict(color='white',size=15),
        bargap=0,
        barmode='overlay',
        
        )



app.layout = html.Div([
    
    
                
    dcc.Graph(figure=fig,style={'backgroundColor':'rgb(1,1,1)'}),
   
],style={'height':'50%'})





  
    
    
    
    
    