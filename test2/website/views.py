from django.shortcuts import render,redirect
from django.http import HttpResponse
import folium
import pandas as pd
from django.views.generic import TemplateView


def route_map(request):
    my_data=pd.read_csv(r"D:\Web Downloads\mostly_taken_route.csv")
    ranks=my_data["Rank"].unique()
    color={"A":"#FF1493",
    "B":'#aa12cc',
    "C":'#0fe3f2'
    }
    dictt={}
    for i in ranks:
        dictt[i]=my_data[my_data["Rank"]==i]
        dictt[i]['color']=color[i]
    tip_marker=[]
    for val in dictt:
        i=dictt[val].iloc[0]['color']
        a=dictt[val]['Lat'].head(1).values.tolist()[0]
        b=dictt[val]['Long'].head(1).values.tolist()[0]
        c=dictt[val]['Location'].head(1).values.tolist()[0]
        tip_marker.append([a,b,c,i])
        d=dictt[val]['Lat'].tail(1).values.tolist()[0]
        e=dictt[val]['Long'].tail(1).values.tolist()[0]
        f=dictt[val]['Location'].tail(1).values.tolist()[0]
        tip_marker.append([d,e,f,i])
    lines=[]
    for val in dictt:
        a=dictt[val].loc[:,['Lat','Long']].values.tolist()
        b=dictt[val].loc[:,['Rank']].values.tolist()[0]
        c=color[val]
        lines.append([a,b,c])
    rankA=dictt["A"]
    rankB=dictt["B"]
    rankC=dictt["C"] 
    rank1=rankA.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist()   #for val in my_data["Rank"].unique():
    rank2=rankB.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist() 
    rank3=rankC.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist() 
     #   df=dictt[val]
  
    data=pd.read_csv('C:/Users/Rimsha khan/Desktop/most_taken_route.csv')
    leaflet_data=data.loc[:,['lat','long','status','device']].values.tolist()#fetching coordinates
    center=[42.986999999999995,-81.215]
    
    context = {'lines':lines,'rank1':rank1,'rank2':rank2,'rank3':rank3,'data':leaflet_data,'center':center,'tip_marker':tip_marker}
    
    return render(request,'route.html',context)


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


    
