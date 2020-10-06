import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import math 
from tracking import functions
session_val=None

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Avg_Weekly_No_Hrs', external_stylesheets=external_stylesheets,)




app.layout = html.Div([
    dcc.RadioItems(
                id="Month",
               
                value='Weekly',
                
                style={'color':'white'},
                ),           
    dcc.Graph(id="chart",style={'backgroundColor':'rgb(1,1,1)'}),
   
],style={'height':'8%','color':'white','backgroundColor':'rgb(1,1,1)'})
@app.expanded_callback(
            Output('chart', 'figure'),
            [Input('Month', 'value')])
def display_value(value,**kwargs):
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
    my_data=functions.fetch_insight(type_,dev,'average_active_no_hours_week')
    val=my_data['Active_hours']
    week=my_data['week_day']
    fig=go.Figure()
    for i in range(0,len(week)):

        no=float(val[i])
        m=round(no,2)

        fig.add_trace(go.Bar(y = [week[i]],
                            x =[val[i]],
                            width=[0.5] ,
                            text='<b>Hours Active: </b>'+str(m),
                            textposition = 'inside',
                            orientation='h',
                            marker_color='red',
                            marker_line_color='red',
                            hovertemplate =
        '<b>Active Hours</b>: %{x}  '+"(hrs)"+'<b> Day</b>: %{y}'
            "<extra></extra>",
                            ))
            
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis={'zeroline': False,'title':'No. of Hours','autorange':True,'showgrid':False,},
        yaxis = dict( zeroline= False,showgrid=False),
        height=300,
        font=dict(color='white'),
        bargap=0,
        barmode='overlay',
        
        )
    fig.update_yaxes( zeroline = False,
  showline = False)
    return fig
    
    