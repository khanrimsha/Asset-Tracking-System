import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Most_Taken_Route', external_stylesheets=external_stylesheets)
my_data=pd.read_csv(r"D:\Web Downloads\mostly_taken_route.csv")




ranks=my_data["Rank"].unique()
color={"A":"#FF1493",
"B":'#aa12cc',
"C":'#0fe3f2'

}
dictt={}
for i in ranks:
    dictt[i]=my_data[my_data["Rank"]==i]
fig = go.Figure()
for val in my_data["Rank"].unique():
    df=dictt[val]

    fig.add_trace(go.Scattermapbox(lat=df['Lat'], lon=df['Long'],
    mode='markers+lines',hovertext="Rank: ",text =df['Location'],name=val,marker=go.scattermapbox.Marker(
            size=20,
            color=color[val],
            opacity=0.5,
        
           
        )
   )) 
    fig.add_trace(go.Scattermapbox(lat=df['Lat'], lon=df['Long'],
mode='markers',marker=go.scattermapbox.Marker(
            size=5,
            color=color[val],
            opacity=0.7,

        )
   ))

fig.update_layout(mapbox_style="carto-darkmatter", mapbox_center_lon=180)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
fig.update_layout(
    
    showlegend=True,
    mapbox=dict(
       
        
        center=dict(
            
            lat=my_data.iloc[1]['Lat'],
            lon=my_data.iloc[1]['Long'],
        ),
        #style='light',
        zoom=12,
    
    ),
)
fig.update_layout(
            paper_bgcolor='rgba(0,0,0)',
            plot_bgcolor='rgb(0,0,0)',
            font=dict(color='white'),
            
            )



app.layout = html.Div([dcc.Graph(figure=fig)
    
])



    