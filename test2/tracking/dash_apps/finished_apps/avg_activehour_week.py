import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from tracking import functions
session_val=None

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('AvgActiveHourWeek', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    dcc.RadioItems(
                id="Month",
               
                value='Weekly',
                
                style={'color':'white'},
                ),
                
    dcc.Graph(id='chart',style={'backgroundColor':'rgb(1,1,1)'}),
   
],style={'height':'50%'})
@app.expanded_callback(

 Output('chart', 'figure'),
  [Input('Month', 'value')]
)
def fun(value,**kwargs):
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
 
    val=[]
    my_data=functions.fetch_insight(type_,dev,'most_active_time_duration_week')
    week=my_data['x'].values.tolist()
    fire_val=my_data['y'].values.tolist()
    for i in range(0,len(fire_val)):
        val.append(functions.convert(fire_val[i]))

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
    return fig




  
    
    
    
    
    