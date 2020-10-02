import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
import folium
from branca.element import Figure
import plotly.express as px
import json
import dash_table
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('MostVisitedLocation', external_stylesheets=external_stylesheets)

geo_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/mostly_visited_location.csv')
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
unique=geo_data['cluster'].unique()
uni=pd.DataFrame()
for i in unique:
    i=pd.Series(geo_data[geo_data['cluster']==i].iloc[0])
    uni=uni.append(i)
uni['size']=100
uni['marker']='marker'
colors=['yellow',
 'yellow',
 'blue',
 'pink',
 'pink',
 'red',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'orange',
 'darkred',
 'darkred',
 'blue',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'red',
 'green',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred',
 'darkred']

app.layout = html.Div([
    html.Div([
        html.Div([
    dcc.Graph(id='map',hoverData={'points': [{'customdata':13.0}]},
    clickData={'points': [{'customdata':-1}]}
    ),
    html.Div(children='''map''')],
        style={'width': '60%', 'display': 'inline-block','backgroundColor': 'rgb(0, 0, 0)',}),
    html.Div([
        html.Div([
            dcc.Graph(id='hover-data'),html.Div(children='''statistics''')]),
            html.Div([
            dash_table.DataTable(id='table',
            
    columns=[{'id': c, 'name': c} for c in ['location','freq']] ,
    
    style_cell={'textAlign': 'left','whiteSpace': 'normal',
        'height': 'auto',},
    style_cell_conditional=[
        {
            
            'textAlign': 'left',
            'backgroundColor': 'rgb(0,0,0)',
        'color': 'white','border': '1px solid grey' 
        }],
    style_as_list_view=True,
    style_header={'backgroundColor': '#8B1717','color': 'white','fontWeight': 'bold'},
    
)
        ])
            ],
    style={'width': '40%', 'display': 'inline-block','backgroundColor': 'rgb(0, 0, 0)'})],
    #exception
    style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(0, 0, 0)',
        'padding': '10px 5px'}
        )
        
        ])
def creategraph(dff):
    
    location=[]
    for i in range(0,len(dff)):
        address=dff['location'][i].split(',')
        add=''
        for i in range(0,len(address)-2):
    
            add=add+str(address[i])
        location.append(add)
    
    values = pd.Series(dff['freq'] )
    figure = go.Figure(data=[go.Pie(labels=location, values=values, textinfo='label+percent',
                             insidetextorientation='radial',hole=0.3,domain = {'x': [0, 1], 'y': [0, 1]},
                            )])
    figure.update_layout(#title_text='<b>Mostly Visited Location</b>',
    autosize=False,
    paper_bgcolor='rgba(0,0,0)',
height = 500,
width = 400,
        plot_bgcolor='rgb(0,0,0)',font=dict(color='white'))
    return figure
    
@app.callback(
   Output('hover-data', 'figure'),
   [Input('map','hoverData')]
    )
def display_hover_data(hoverData):
    my=hoverData['points'][0]['customdata']
    dff=geo_data[geo_data['cluster'] == my].reset_index(drop=True)
    return (creategraph(dff))
@app.callback(
   Output('table', 'data'),
   [Input('map','hoverData')]
    )
def display_data(hoverData):
    my=hoverData['points'][0]['customdata']
    dff=geo_data[geo_data['cluster'] == my].reset_index(drop=True)
    new_df=dff[['location', 'freq']]
    return (new_df.to_dict('records'))
def createmap(dff,my):
    #if my!= -1:
        #i=dff.loc[dff.cluster == my, 'lat_center']
        #j=dff.loc[dff.cluster == my, 'long_center']
    #else:
        #i=dff.iloc[0]['lat_center']
        #j=dff.iloc[0]['long_center']
    dff['symbol']='circle'
    fig=go.Figure(go.Scattermapbox(
        lat = dff.lat_center,
        lon = dff.long_center,
        
        customdata=dff['cluster'],
        mode = 'markers',
        text=dff['location'],
        marker=dict(size=dff['size'],
        sizemode= 'area',
        colorscale=[[0, 'rgb(200,0,0)'], [1, 'rgb(0,200,0)']],
        
        showscale=True, # show color scale False for hiding
                    color= dff.cluster_freq,
                    opacity = 0.7)))
    fig.update_layout(mapbox_style="open-street-map",paper_bgcolor='rgba(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',font=dict(color='white'))
    fig.update_layout(
    
    
    mapbox=dict(
        
        center=dict(
            lat=dff.iloc[0]['lat_center'],
        lon=dff.iloc[0]['long_center'],
            
        ),
        
        zoom=10,
    
    ),
)
    
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
@app.callback(
   Output('map', 'figure'),
   [Input('map','clickData')]
    )
def click(clickData):
    my=clickData['points'][0]['customdata']
    if my!= -1:
        my_colors=colors.copy()
        my_colors[-1]='blue'
        dff=geo_data[geo_data['cluster'] == my].reset_index(drop=True)#extracting new points
        dff['lat_center']=dff['lat']
        dff['long_center']=dff['long']
        dff['size']=10
        dff['marker']='marker'
        my_dff=uni
        my_dff.loc[my_dff.cluster == my, 'size'] = 100
        for i in range(0,len(dff)):
            my_dff=my_dff.append(dff.iloc[i])#making new df    
        

        #for n in range(1,len(dff)):
            #my_colors.append('blue')
        
        return (createmap(my_dff,my))
    else:
        
        return (createmap(uni,my))



 

    


