import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from firebase import firebase
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import json
try:
    cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
    firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
except:
    pass
database=db.reference("car/KC7LZD-9/insights/Fuel_consumed_date/")
d=database.get()
data_json = json.loads(d)
fuel_used=pd.DataFrame(data_json)
fuel_used["DATE"]=fuel_used["DATE"].apply(lambda x: datetime.datetime.fromtimestamp(x//1000).strftime('%Y-%m-%d'))
fuel_used['DATE'] = pd.to_datetime(fuel_used.DATE)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('FuelDate', external_stylesheets=external_stylesheets)

options=['All','January','February','March','April','May','June','July','August','September','October','November','December']
Date=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
month_no=['01','02','03','04','05','06','07','08','09','10','11','12']

app.layout = html.Div([
  
    dcc.Dropdown(
                id="Month",
                options=[{
                    'label': i,
                    'value': i
                } for i in options],
                value='January',
                ),
                
    dcc.Graph(id='slider-graph',style={'backgroundColor':'rgb(1,1,1)'}),
   
])

def gen_traces(selected_name):
    if selected_name=='All':
        rimsha=fuel_used
    else:
        month=month_no[options.index(selected_name)-1]
        rimsha=pd.DataFrame(columns=['DATE','FUEL_USED'])
        for i in Date:
            date='2020-'+month+'-'+i
            rimsha=rimsha.append(fuel_used[fuel_used['DATE']==date])
    traces = {}
    traces['graph']=[go.Bar(x = rimsha['DATE'],
                        y = rimsha["FUEL_USED"],
                        marker_line_color='#FFA200',
                        marker_line_width=1.5,
                        marker_color='#FFA200',
                        opacity=0.8,
                        
                        )]
    traces['layout'] =go.Layout(
        
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'autorange':True},
        
        yaxis = dict(range=[0,5],title='Fuel Consumed(in litres)'),
        #title="Daily Fuel Consumed",
        font=dict(color='white'),
           
        )
    return traces

@app.callback(
            Output('slider-graph', 'figure'),
            [Input('Month', 'value')])
def display_value(Month):
    
    data=gen_traces(Month)
    return {'data': data['graph'],'layout' :data['layout']}
   
    