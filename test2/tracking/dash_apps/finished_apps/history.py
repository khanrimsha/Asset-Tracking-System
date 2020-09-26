import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import dash_table
from tracking import functions
from datetime import datetime as dt
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('history', external_stylesheets=external_stylesheets)

session_val=None



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
        min_date_allowed=dt(2020, 1, 26),
        max_date_allowed=dt.today().date(),
        initial_visible_month=dt.today().date(),
        end_date=dt(2020, 10, 26).date(),
    ),
    html.Div(id='output-container-date-picker-range')
]),
       
        html.Div([
            dash_table.DataTable(id='table',
            
    columns=[{'id': c, 'name': c} for c in ['DATE','TIME','LATITUDE','LONGITUDE','SPEED']] ,
    
    style_cell={'textAlign': 'left'},
    style_cell_conditional=[
        {
            
            'textAlign': 'left',
            'backgroundColor': 'rgb(255,255,255)',
        'color': 'black'
        }],
    style_as_list_view=True,
    style_header={'backgroundColor': '#add8e6','color': 'black'},
    
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
     Input('my-date-picker-range', 'end_date')]
)
def fun(start_date, end_date,**kwargs):
    dates={
        'start_date':start_date,'end_date':end_date
    }
    global session_val
    session_val=kwargs["session_state"]
    geo_data=functions.get_data(session_val,dates)
    
    
    return(geo_data.to_dict('records'))





    


