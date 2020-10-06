import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import datetime
from tracking import functions
session_val=None

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
                value='May',
                ),
                
    dcc.Graph(id='slider-graph',style={'backgroundColor':'rgb(1,1,1)'}),
   
])

def gen_traces(selected_name,fuel_used):
    if selected_name=='All':
        data=fuel_used
    else:
        month=month_no[options.index(selected_name)-1]
        data=pd.DataFrame(columns=['DATE','FUEL_USED'])
        for i in Date:
            date='2020-'+month+'-'+i
            data=data.append(fuel_used[fuel_used['DATE']==date])
    traces = {}
    traces['graph']=[go.Bar(x = data['DATE'],
                        y = data["FUEL_USED"],
                        marker_line_color='#FFA200',
                        marker_line_width=1.5,
                        marker_color='#FFA200',
                        opacity=0.8,
                        
                        )]
    traces['layout'] =go.Layout(
        
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'autorange':True,'title':'Date'},
        
        yaxis = dict(range=[0,data["FUEL_USED"].max()],title='Fuel Consumed(in litres)'),
        #title="Daily Fuel Consumed",
        font=dict(color='white'),
           
        )
    return traces

@app.expanded_callback(
            Output('slider-graph', 'figure'),
            [Input('Month', 'value')])
def display_value(Month,**kwargs):
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
    fuel_used=functions.fetch_insight(type_,dev,'Fuel_consumed_date')
    fuel_used["DATE"]=fuel_used["DATE"].apply(lambda x: datetime.datetime.fromtimestamp(x//1000).strftime('%Y-%m-%d'))
    fuel_used['DATE'] = pd.to_datetime(fuel_used.DATE)
    
    data=gen_traces(Month,fuel_used)
    return {'data': data['graph'],'layout' :data['layout']}
   
    