import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('AvgActiveHourDate', external_stylesheets=external_stylesheets)

fuel_used=pd.read_csv('C:/Users/Rimsha khan/Desktop/insights/insights/Activehours_date.csv')
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
        rimsha=pd.DataFrame(columns=['DATE','Active_hours'])
        for i in Date:
            date='2020-'+month+'-'+i
            rimsha=rimsha.append(fuel_used[fuel_used['DATE']==date])
    traces = {}
    traces['graph']=[go.Bar(x = rimsha['DATE'],
                        y = rimsha["Active_hours"],
                        marker_line_color='#0060CC',
                        marker_line_width=2,
                        marker_color='#99CCFF',
                        opacity=0.8,
                        
                        )]
    traces['layout'] =go.Layout(
        
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        
       # xaxis={'autorange':True,'title':'Date','fixedrange':True},
        xaxis = dict(title='Date',type='date'),
        yaxis = dict(range=[0,fuel_used['Active_hours'].max()],title='Hours'),
        title="Average Active Hours",
        font=dict(color='white'),
           
        )

    return traces

@app.callback(
            Output('slider-graph', 'figure'),
            [Input('Month', 'value')])
def display_value(Month):
    
    data=gen_traces(Month)
    return {'data': data['graph'],'layout' :data['layout']}
   
    