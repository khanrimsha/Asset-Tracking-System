from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views import View
import pandas as pd
import csv
import json
import os
import folium
import pandas as pd
from django.views.generic import TemplateView
username1="rimsha"
password1="khan"
# Create your views here.
def index(request):
    return render(request,'index.html',{})
def logout(request):
   
    return render(request,'logout.html',{})


def leaf(request):
    data=pd.read_csv('C:/Users/Rimsha khan/Desktop/most_taken_route.csv')
    leaflet_data=data.loc[:,['lat','long','status','device']].values.tolist()#fetching coordinates
    center=[48.0295, -122.992]
    danger=data[data['status']=='Danger']
    prob=danger['Prob'].values.tolist()
    device=danger['device'].values.tolist()
    danger_data=danger.loc[:,['lat','long']].values.tolist()
    my='Rimsha'
    context = {'data':leaflet_data,'center':center,'danger':danger,'danger_data':danger_data,'prob':prob,'device':device,'my':my}
    
    return render(request,'leaflet.html',context)

def my_data(request):
    with open('D:/django/test2/website/data/data.json',mode='r') as j:
        my=json.load(j)
    return HttpResponse(my,content_type='json')
def maps(request):
    return render(request,'maps.html',{})
def login(request):
    if request.method=="POST":
           
        username=request.POST['username']
        password=request.POST['pass']
        if username==username1 and password == password1:
            
            return render(request,'tracking/test.html',{})
        else:
            return render(request,'./home.html',{})
    else:
        return render(request,'./home.html',{})
def folium_map(request):
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
    return render(request,'./maps.html',context)


    
