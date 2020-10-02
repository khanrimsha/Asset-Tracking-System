import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from tracking import functions
session_val=None


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('FuelWeek', external_stylesheets=external_stylesheets)

options=['Monthly','Weekly']
Date=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
month_no=['01','02','03','04','05','06','07','08','09','10','11','12']
fuel_used_month=pd.read_csv('C:/Users/Rimsha khan/Desktop/insights/insights/fuelused_date.csv')
month=['Jan','Feb','March','April',"May",'June','July','August','Sept','Oct','Nov','Dec']
val2=[2,8,9,3,10,7,9,12,10,8,9,15]
app.layout = html.Div([
    
    dcc.RadioItems(
                id="Month",
               
                value='Weekly',
                
                style={'color':'white'},
                ),
                
    dcc.Graph(id='slider-graph',style={'backgroundColor':'rgb(1,1,1)'}),
   
])



@app.expanded_callback(
            Output('slider-graph', 'figure'),
            [Input('Month', 'value')])
def display_value(value,**kwargs):
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
 
    fuel_used_week=functions.fetch_insight(type_,dev,'Fuel_consumed_week')
    
    if value=='Weekly':
        
        x= fuel_used_week['week_day']
        y = fuel_used_week["FUEL_USED"]
    else:
        x=month
        y=val2
    fig=go.Figure()
    fig.add_trace(go.Bar({'x' :x,
                        'y' : y,
                        'marker_line_color':'#CC0066',
                        'marker_line_width':1.5,
                        'marker_color':'#CC0066',
                        'opacity':0.8,
                        'name':'Weekly',
                        
        }))
    
    
    
    fig.update_layout(
        
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'autorange':True,'showgrid':False,'title':'Days'},
        yaxis = dict(title='Fuel Consumed(in litres)',showgrid=False),
        #title={'text':"Average Fuel Consumed "+value+'<i> (approx) </i>', 'y':0.9,
        #'x':0.5,
        #'xanchor': 'center',
        #'yanchor': 'top'},
        font=dict(color='white'),
        showlegend=False,
        )
    
    return (fig)
    
   
    