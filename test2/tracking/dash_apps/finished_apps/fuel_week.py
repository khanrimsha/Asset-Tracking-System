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
  
    x= fuel_used_week['week_day']
    y = fuel_used_week["FUEL_USED"]
    
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
    
   
    