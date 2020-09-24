from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import functions
import folium
import numpy
import pandas as pd
from website import views
username1="rimsha"
password1="khan"

dev_name="rimsha"
def login(request):
    if request.method=="POST":
                 
        username=request.POST['username']
        password=request.POST['pass']
        if username==username1 and password==password1 :
            session = request.session
            request.session['username'] = username
            request.session['pass'] = password
            request.session['dev_name']="No Select"
            #demo_count = session.get('django_plotly_dash', {})
            #demo_count= 'KHIZT'
            session['django_plotly_dash'] = 'KHIZT' #random vehicle name
            return redirect('tracking/')
        else:
            return render(request,'tracking/home.html')
    else:
        return render(request,'tracking/home.html')
def logout(request):
    try:
        del request.session['django_plotly_dash']
        del request.session['username']
        del request.session['pass']
        del request.session['dev_name']
    except:
        pass
    return render(request,'tracking/logout.html',{})
def tracking(request):
    if request.session.has_key('username') and request.session.has_key('pass'):
        if request.session['username']==username1 and request.session['pass']==password1 :
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
            my_var=functions.var()
            context = {'my_map': m,'my_var':my_var}
            return render(request,'tracking/test.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')
def veh_hist(requests):

    if requests.session.has_key('username') and requests.session.has_key('pass'):
        if requests.session['username']==username1 and requests.session['pass']==password1 :
            m2=functions.history_map()
            functions.change_var('KI7MH-7')
            drop=functions.vehicle_drop('car')
            
            results='No Select'
        
            if requests.method=="POST":
                results=requests.POST['cars'] #name of select
            context = {'mymap': m2,'drop':drop,'val':results}
            return render(requests,'tracking/vehicle_history.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')

def insights(request):
    if request.session.has_key('username') and request.session.has_key('pass'):
        if request.session['username']==username1 and request.session['pass']==password1 :
           
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
        
            if request.method=="POST":
                results=request.POST['cars'] #name of select
                request.session['dev_name']=results
                request.session['django_plotly_dash']=results

              
            results=request.session['dev_name']
            drop=functions.vehicle_drop('car') 
            
            context = {'mymap': m2,'drop':drop,'val':results}
            return render(request,'tracking/insights.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')

def collision_detection(request):
    if request.session.has_key('username') and request.session.has_key('pass'):
        if request.session['username']==username1 and request.session['pass']==password1 :
            results='No Select'
            plane_name=7865317
            if request.method=="POST":
                results=request.POST['cars'] #name of select
                plane_name=request.POST['cars']
            data=functions.col_det(plane_name)
            leaflet_data=data.loc[:,['lat','long','status','device','Prob']].values.tolist()#fetching coordinates
            table_data=numpy.transpose(leaflet_data)
            center=[48.0295, -122.992]
            danger=data[data['status']=='Danger']
            prob=danger['Prob'].values.tolist()
            device=danger['device'].values.tolist()
            danger_data=danger.loc[:,['lat','long']].values.tolist()            
            drop=functions.plane_drop()
            context = {'data':leaflet_data,'plane_name':plane_name,'center':center,'table_data':table_data,'danger_data':danger_data,'prob':prob,'device':device,'drop':drop,'val':results}
            
            return render(request,'tracking/collision_detection.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')
