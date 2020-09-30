import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
y=['12am-1am','1am-2am','2am-3am','3am-4am','4am-5am','5am-6am','6am-7am','7am-8am','8am-9am','9am-10am','10am-11am','11am-12pm','12pm-1pm','1pm-2pm','2pm-3pm','3pm-4pm','4pm-5pm','5pm-6pm','6pm-7pm','7pm-8pm','8pm-9pm','9pm-10pm','10pm-11pm','11pm-12am']
app = DjangoDash('MostActiveHour', external_stylesheets=external_stylesheets)
my_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/most_active_hour.csv')
fig = go.Figure()
fig.add_trace(go.Scatter(x=y, y=my_data['Activation_count'],hovertemplate =
    '<b>Frequency</b>: %{y}'+
        "<extra></extra>"
    
    , fill='tozeroy',marker_color='#FF99FF')) 
#fig = px.line(my_data, x='hour', y='Activation_count')


fig.update_layout(xaxis={'title':'<b>Hour</b>'},
        yaxis={'title':'<b>Hour Count</b>'},font_family="Times New Roman",template="simple_white",
        title={
        
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font=dict(color='white'),
        
        )
fig.update_xaxes(range=['12am-1am', '11pm-12am'])
fig.update_yaxes(range=[0,my_data['Activation_count'].max() ])
fig.update_xaxes(fixedrange=True)

app.layout = html.Div([dcc.Graph(figure=fig)
    
])



    