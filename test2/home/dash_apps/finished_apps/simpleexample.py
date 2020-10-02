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

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
week=my_data['x']
val=my_data['y']
day=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
y=['12am-1am','1am-2am','2am-3am','3am-4am','4am-5am','5am-6am','6am-7am','7am-8am','8am-9am','9am-10am','10am-11am','11am-12pm','12pm-1pm','1pm-2pm','2pm-3pm','3pm-4pm','4pm-5pm','5pm-6pm','6pm-7pm','7pm-8pm','8pm-9pm','9pm-10pm','10pm-11pm','11pm-12am']

fig=go.Figure()

for i in range(0,len(week)):
        fig.add_trace(go.Bar(y = [week[i]],
                        x =[y[i]],
                        
                       
                        marker_color='black',
                        marker_line_color='black',
                        hovertemplate =
    '<b>Active Hours</b>: %{x}  '+'<b>Day</b>: %{y}'+
        "<extra></extra>",
                        ))
        if week[i]=='Monday':
            b=0
        if week[i]=='Tuesday':
            b='Monday'
        if week[i]=='Wednesday':
            b='Tuesday'
        if week[i]=='Thursday':
            b='Wednesday'
        if week[i]=='Friday':
            b='Thursday'
        if week[i]=='Saturday':
            b='Friday'
        if week[i]=='Sunday':
            b='Saturday'
        fig.add_shape(
        # filled Rectangle
            type="rect",
            x0=str(val[i]),
            y0=week[i],
            x1=int(val[i])-1,
           
            y1=b,
            line=dict(
                color="#F9D212",
                width=4,
            ),
            fillcolor="#F9D212",
            opacity=0.8,
            
        )
fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'title':'Days','autorange':True,'showgrid':False,'fixedrange':True},
        yaxis = dict(title='hi',showgrid=False,fixedrange=True),
        
        font=dict(color='white',size=15),
        bargap=0,
        barmode='overlay',
        
        )



app.layout = html.Div([
    
    
                
    dcc.Graph(figure=fig,style={'backgroundColor':'rgb(1,1,1)'}),
   
],style={'height':'50%'})





  
    
    
    
    
    