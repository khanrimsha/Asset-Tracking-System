import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import dash_table
import plotly.express as px
from tracking import functions
from datetime import datetime, timedelta
import re
import folium

map_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')

map_data=map_data.dropna(subset=['LATITUDE','LONGITUDE'])
map_data=map_data[map_data['DATE']=='2020-06-07']
Lat=map_data["LATITUDE"].values.tolist()
Long=map_data["LONGITUDE"].values.tolist()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('history', external_stylesheets=external_stylesheets,)
mapbox_access_token ="pk.eyJ1FFRitFm5rLQihCFPSNPkwLNBTbVZHUAnYc5iRYaWz9emMnBwZjdzeTR1YWhxIn0.OemloU9jL19pl6zCBYG22Q"
session_val=None
figdata=None
def create_map(dff,start,end):
   

    try:

        listt=dff.loc[:,['LATITUDE','LONGITUDE']].values.tolist()
        last_co_ords=dff.loc[:,['LATITUDE','LONGITUDE']].tail(1).values.tolist()
        m2=folium.Map(location=listt[0],zoom_start=8,tiles='cartodbpositron',attr='Vehicle Track')
        if start is None:
            folium.vector_layers.PolyLine(listt,popup='<b>Path of Vehicle</b>',tooltip='<strong>Date: </strong>'+str(end),color='blue',weight=3).add_to(m2)
        else:
            folium.vector_layers.PolyLine(listt,popup='<b>Path of Vehicle</b>',tooltip='<strong>From: </strong>'+str(start)+'<strong> To: </strong>'+str(end),color='blue',weight=3).add_to(m2)
        
        folium.Marker(location=listt[0],popup='Starting Point',tooltip='<strong>Starting Point</strong>',icon=folium.Icon(color='red',prefix='fa',icon='anchor')).add_to(m2)
        folium.Marker(location=last_co_ords[0],popup='Finish Point',tooltip='<strong>Finish Point</strong>',icon=folium.Icon(color='purple',prefix='fa',icon='anchor')).add_to(m2)
    except:
        m2=folium.Map(zoom_start=8,tiles='cartodbpositron',attr='Vehicle Track')

    m2.save('C:/Users/Rimsha khan/Desktop/firebase_map.html')
    

PAGE_SIZE=12
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


app.layout = html.Div([
    
 html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=datetime(2020,1,16),
        max_date_allowed=datetime.today()-timedelta(days=1),
        initial_visible_month=datetime.today()-timedelta(days=1),
        end_date=datetime.today()-timedelta(days=1)
    ),
    html.Div([
        html.Iframe(id='map' ,width="960" ,height="500"),

    ],style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(0, 0, 0)',
        'padding': '10px 5px','height':'500px'}),
    html.Div(id='output-container-date-picker-range')
]),
       
        html.Div([
            dash_table.DataTable(id='table',
            page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',
    columns=[{'id': c, 'name': c} for c in ['DATE','TIME','LATITUDE','LONGITUDE','SPEED']] ,
   
    style_cell={'textAlign': 'left','backgroundColor': '#5c404e'},
    style_cell_conditional=[
        {
            
            'textAlign': 'left',
            'backgroundColor': '#f5bfd6',
        
        'font':{'color':'black','size':'15px'},
        
        }],
    style_as_list_view=True,
    style_header={'height':'20px','backgroundColor': '#d41e7c','color': 'white','fontWeight': 'bold',},
    
),

        ])
        ])
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@app.expanded_callback(

 Output('table', 'data'),
   [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('table', "page_current"),
     Input('table', "page_size"),
     ]
)
def fun(start_date, end_date,page_current,page_size,**kwargs):
    enddate = datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
    enddate=enddate.strftime('%Y-%m-%d')
    try:
        startdate = datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        startdate=startdate.strftime('%Y-%m-%d')
     
    except:
        startdate=start_date
    
    dates={
        'start_date':startdate,'end_date':enddate
    }
    global session_val,figdata
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
    geo_data=functions.get_data(type_,dev,dates)
    figdata=functions.get_data(type_,dev,dates)
    if geo_data is None:
        return html.Div([
            html.H1(children='No data to Show'),
        ],style={'color':'white'}
            )
    else:


        return geo_data.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records')
    
@app.expanded_callback(

 Output('map', 'srcDoc'),
   [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
   
     ]
)
def map_(start_date, end_date,**kwargs):
    enddate = datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
    enddate=enddate.strftime('%Y-%m-%d')
    try:
        startdate = datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        startdate=startdate.strftime('%Y-%m-%d')
     
    except:
        startdate=start_date
    
    dates={
        'start_date':startdate,'end_date':enddate
    }
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
    figdata=functions.get_data(type_,dev,dates)
    
    create_map(figdata,startdate,enddate)
    return open('C:/Users/Rimsha khan/Desktop/firebase_map.html','r').read()




    


