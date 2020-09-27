import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import dash_table
from tracking import functions
from datetime import datetime, timedelta
import re


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('history', external_stylesheets=external_stylesheets)

session_val=None


PAGE_SIZE=30
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
    global session_val
    session_val=kwargs["session_state"]
    dev=session_val['dev']
    type_=session_val['car/truck'].lower()
    geo_data=functions.get_data(type_,dev,dates)
    if geo_data is None:
        return html.Div([
            html.H1(children='No data to Show'),
        ],style={'color':'white'}
            )
    else:


        return geo_data.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records')
    





    


