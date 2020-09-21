from django.shortcuts import render
from django.http import HttpResponse
import folium
import numpy
import pandas as pd
from django.http import HttpResponse
def tracking(request):
    url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
    my_data=pd.read_csv('D:/django/test2/website/data/point.csv')
    m = folium.Map(location=[20, 0], tiles=url,attr='by Rimsha Khan',zoom_start=2)
    for i in range(0,len(my_data)):
        if my_data.iloc[i]['type']=='plane':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/my_plane.png',icon_size=(25,25))
        if my_data.iloc[i]['type']=='car':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/car-icon.png',icon_size=(25,25))
        folium.Marker([my_data.iloc[i][1], my_data.iloc[i][2]], popup=my_data.iloc[i][0],icon=logo_icon).add_to(m),
    m=m._repr_html_() #updated
    context = {'my_map': m}
    return render(request,'tracking/test.html',context)

def veh_hist(requests):
    geo_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')

    geo_data=geo_data.dropna(subset=['LATITUDE','LONGITUDE'])
    my_data=geo_data[geo_data['DATE']=='2020-06-07']
    listt=my_data.loc[:,['LATITUDE','LONGITUDE']].values.tolist()
    last_co_ords=my_data.loc[:,['LATITUDE','LONGITUDE']].tail(1).values.tolist()
    m2=folium.Map(height=200,location=listt[0],zoom_start=6,tiles='cartodbpositron',attr='by Rimsha Khan')

    folium.vector_layers.PolyLine(listt,popup='<b>Path of Vehicle</b>',tooltip='Track of 2020-06-07',color='blue',weight=3).add_to(m2)

    folium.Marker(location=listt[0],popup='Starting Point',tooltip='<strong>Starting Point</strong>',icon=folium.Icon(color='red',prefix='fa',icon='anchor')).add_to(m2)
    folium.Marker(location=last_co_ords[0],popup='Finish Point',tooltip='<strong>Finish Point</strong>',icon=folium.Icon(color='purple',prefix='fa',icon='anchor')).add_to(m2)
    m2=m2._repr_html_()
    context = {'mymap': m2}


    return render(requests,'tracking/vehicle_history.html',context)
def insights(request):
    geo_data=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')

    geo_data=geo_data.dropna(subset=['LATITUDE','LONGITUDE'])
    my_data=geo_data[geo_data['DATE']=='2020-06-07']
    listt=my_data.loc[:,['LATITUDE','LONGITUDE']].values.tolist()
    last_co_ords=my_data.loc[:,['LATITUDE','LONGITUDE']].tail(1).values.tolist()
    m2=folium.Map(height=300,location=listt[0],zoom_start=6,tiles='cartodbpositron',attr='by Rimsha Khan')

    folium.vector_layers.PolyLine(listt,popup='<b>Path of Vehicle</b>',tooltip='Track of 2020-06-07',color='blue',weight=3).add_to(m2)

    folium.Marker(location=listt[0],popup='Starting Point',tooltip='<strong>Starting Point</strong>',icon=folium.Icon(color='red',prefix='fa',icon='anchor')).add_to(m2)
    folium.Marker(location=last_co_ords[0],popup='Finish Point',tooltip='<strong>Finish Point</strong>',icon=folium.Icon(color='purple',prefix='fa',icon='anchor')).add_to(m2)
    m2=m2._repr_html_()
    results='No Select'
    drop=['Car','Truck']
    if request.method=="POST":
        results=request.POST['cars'] #name of select
    
        
    drop=['KI7MH','dummy'] 
    context = {'mymap': m2,'drop':drop,'val':results}
    return render(request,'tracking/insights.html',context)
#def my_page(request):
    #results=request.GET['cars'] #name of select
    #return render(request,'tracking/my_page.html',{'val':results})
def collision_detection(request):
    data=pd.read_csv('C:/Users/Rimsha khan/Desktop/most_taken_route.csv')
    leaflet_data=data.loc[:,['lat','long','status','device','Prob']].values.tolist()#fetching coordinates
    table_data=numpy.transpose(leaflet_data)
    center=[48.0295, -122.992]
    danger=data[data['status']=='Danger']
    prob=danger['Prob'].values.tolist()
    device=danger['device'].values.tolist()
    danger_data=danger.loc[:,['lat','long']].values.tolist()
    results='No Select'
   
    if request.method=="POST":
        results=request.POST['cars'] #name of select
    
        
    drop=['KI7MH','dummy']
    context = {'data':leaflet_data,'center':center,'table_data':table_data,'danger_data':danger_data,'prob':prob,'device':device,'drop':drop,'val':results}
    
    return render(request,'tracking/collision_detection.html',context)