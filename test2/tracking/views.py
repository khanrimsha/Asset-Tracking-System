from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import functions
import folium
import numpy
import pandas as pd
from website import views
username1="group_43"
password1="cis"
car_count=functions.car_count
truck_count=functions.truck_count
plane_count=4067
vehicle_count=car_count+truck_count+plane_count
car_name="rimsha"
def login(request):
    if request.method=="POST":
                 
        username=request.POST['username']
        password=request.POST['pass']
        if username==username1 and password==password1 :
            session = request.session
            request.session['username'] = username
            request.session['pass'] = password
           
            request.session['car_name']="KC7LZD-9"
            request.session['plane']=7668253
            request.session['truck_name']="KE4KMD-14"
            request.session['car/truck']='Car'
            request.session['live_track']='False'
            #demo_count = session.get('django_plotly_dash', {})
            #demo_count= 'KHIZT'
            initial={'dev':'KC7LZD-9','car/truck':'Car'}
            session['django_plotly_dash'] = initial #random vehicle name
            return redirect('tracking/')
        else:
            return render(request,'tracking/home.html')
    else:
        return render(request,'tracking/home.html')
def logout(request):
    try:
        del request.session['django_plotly_dash']
        del request.session['car/truck']
        del request.session['username']
        del request.session['pass']
        del request.session['plane']
        del request.session['car_name']
        del request.session['truck_name']
        del request.session['live_track']
    except:
        pass
    return render(request,'tracking/logout.html',{})
def tracking(request):
    if request.session.has_key('username') and request.session.has_key('pass'):
        if request.session['username']==username1 and request.session['pass']==password1 :
            
            track="False"
            try:
                track=request.POST['live-track']
                request.session['live_track']=track
            except:
                pass
                
            track=request.session['live_track']
            
            if track=='False':
                m=functions.firebase_location()
                print("I am firebase")
            else:
                m=functions.current_location()
                print('I am post')
            
            request.session['live_track']='False'
            context = {'my_map': m,'truck_count':truck_count,'car_count':car_count,'plane_count':plane_count,'vehicle_count':vehicle_count}
            return render(request,'tracking/index.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')
def veh_hist(requests):

    if requests.session.has_key('username') and requests.session.has_key('pass'):
        if requests.session['username']==username1 and requests.session['pass']==password1 :
       
            
         
            results='No Select'
            
            try:
                
                car_truck=requests.GET['car_truck']
                requests.session['car/truck']=car_truck
            
            except:
                pass
            car_truck=requests.session['car/truck']
            requests.session['django_plotly_dash']['car/truck']=car_truck
            drop=functions.vehicle_drop(car_truck)
            #requests.session['car_name']=results
            #results=requests.session['django_plotly_dash']
            if requests.method=="POST":
               
                results=requests.POST['cars'] #name of select
              
                
                if car_truck=='Car':
                    requests.session['car_name']=results
                    
                else:
                    requests.session['truck_name']=results
            if car_truck=='Car':
                requests.session['django_plotly_dash']['dev']=requests.session['car_name']
                display='Truck'   
            else:
                requests.session['django_plotly_dash']['dev']=requests.session['truck_name']
                display='Car'
            
                
            results=requests.session['django_plotly_dash']['dev']

            context = {'drop':drop,'val':results,'ct':car_truck,'car_count':car_count,'truck_count':truck_count,'plane_count':plane_count,'vehicle_count':vehicle_count,'display':display}
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
            try:
                
                car_truck=request.GET['car_truck']
                request.session['car/truck']=car_truck
            
            except:
                pass
            car_truck=request.session['car/truck']
            request.session['django_plotly_dash']['car/truck']=car_truck
            drop=functions.vehicle_drop(car_truck)
            #requests.session['car_name']=results
            #results=requests.session['django_plotly_dash']
            if request.method=="POST":
               
                results=request.POST['cars'] #name of select
               
                
                if car_truck=='Car':
                    request.session['car_name']=results
                    
                else:
                    request.session['truck_name']=results
            if car_truck=='Car':
                request.session['django_plotly_dash']['dev']=request.session['car_name']
                display='Truck'   
            else:
                request.session['django_plotly_dash']['dev']=request.session['truck_name']
                display='Car'
            
            name=request.session['django_plotly_dash']['dev']
            type_=request.session['django_plotly_dash']['car/truck']
            my_data=functions.fetch_insight(type_,name,"mostly_taken_route")
            #my_data=pd.read_csv(r"D:\Web Downloads\mostly_taken_route.csv")
            ranks=my_data["Rank"].unique()
            color={"A":"#FF1493",
            "B":'#aa12cc',
            "C":'#0fe3f2'
            }
            dictt={}
            max_limit=my_data['freq'].max()
            indicator=[]
            for i in ranks:
                dictt[i]=my_data[my_data["Rank"]==i]
                dictt[i]['color']=color[i]
                indicator.append([my_data[my_data["Rank"]==i].iloc[0]['freq'],i,max_limit])
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
            try:
                rankB=dictt["B"]
            except:
                rankB="None"
            try:
                rankC=dictt["C"] 
            except:
                rankC="None"
            try:
                rank1=rankA.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist()   #for val in my_data["Rank"].unique():
            except:
                rank1=0
            try:
                rank2=rankB.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist() 
            except:
                rank2=0
            try:
                rank3=rankC.loc[:,['Rank','Lat','Long','color','Location','freq']].values.tolist() 
            except:
                rank3=0

 
            results=request.session['django_plotly_dash']['dev']
            context = {'indicator':indicator,'lines':lines,'rank1':rank1,'rank2':rank2,'rank3':rank3,'tip_marker':tip_marker,'mymap': m2,'drop':drop,'val':results,'car_count':car_count,'truck_count':truck_count,'plane_count':plane_count,'vehicle_count':vehicle_count,'display':display}
            
            return render(request,'tracking/insights.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')

def collision_detection(request):
    if request.session.has_key('username') and request.session.has_key('pass'):
        if request.session['username']==username1 and request.session['pass']==password1 :
           
        
            if request.method=="POST":
                results=request.POST['plane']
                request.session['plane']=results
                 #name of select
               
            plane_name=request.session['plane']
            results=plane_name
            fetched_data=functions.col_det(int(plane_name))
            data=fetched_data['data']
            leaflet_data=data.loc[:,['Latitude','Longitude','Status','Id','Probability','ETC','Altitude', 'Speed', 'Angle',
       'Horizontal_Separation', 'Vertical_Separation', 
       'Horizontal_Position','Vertical_Position',]].values.tolist()#fetching coordinates

            center=fetched_data['center']
            danger=data[data['Status']=='Danger']
            prob=danger['Probability'].values.tolist()
            device=danger['Id'].values.tolist()
            danger_data=danger.loc[:,['Latitude','Longitude']].values.tolist()           
            drop=functions.plane_drop()
            context = {'data':leaflet_data,'plane_name':plane_name,'center':center,'danger_data':danger_data,'prob':prob,'device':device,'drop':drop,'val':results}
            
            return render(request,'tracking/collision_detection.html',context)
        else:
            return redirect('/')
    else:
        
        return redirect('/')
