import folium
import numpy
import pandas as pd
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import datetime
import json
from io import StringIO
import math
import time
import random
import datetime
import requests

vehicle_names={
    'Car':["KC7LZD-9","KI7MH-7","SJ2W-9","SM5RVH-9","VA3MSV-9","VE3TEJ-15"],
    'Truck':['KE4KMD-14','KD5TBX-14','KC0HT-14','N3EOP-14','K7VR-14','N7QIN-14','PD1HPB-14','KN4JUU-14','F4IKQ-9','WB0HBJ-14','SP4XKS-5','KE8WES-14','KE6UWJ-14','KC2HTC-14']

}
car_count=len(vehicle_names['Car'])
truck_count=len(vehicle_names['Truck'])
def convert(a):
   
    if a == 0:
        b="12am-1am"
    elif a == 1:

        b="1am-2am"
    elif a == 2:
        b="2am-3am"
    elif a == 3:
        b="3am-4am"
    elif a == 4:
        b="4am-5am"
    elif a == 5:
        b="5am-6am"
    elif a == 6:
        b="6am-7am"
    elif a == 7:
        b="7am-8am"
    elif a == 8:
        b="8am-9am"
    elif a == 9:
        b="9am-10am"
    elif a == 10:
        b="10am-11am"
    elif a == 11:
        b="11am-12pm"

    elif a == 12:
        b="12pm-1pm"   
    elif a == 13:
        b="1pm-2pm"    
    elif a == 14:
        b="2pm-3pm"
    elif a == 15:
        b="3pm-4pm"    
    elif a == 16:
        b="4pm-5pm"
    elif a == 17:
        b="5pm-6pm"
    elif a == 18:
        b="6pm-7pm"
    elif a == 19:
        b="7pm-8pm"
    elif a == 20:
        b="8pm-9pm"
    elif a == 21:
        b="9pm-10pm"
    elif a == 22:
        b="10pm-11pm"
    elif a == 23:
        b="11pm-12am"
    else:
        b=None
    return(b)
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6378.1 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d


def distance_3d(origin, destination,alt1,alt2):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6378.1 # km
    alt1=alt1*0.0003048
    alt2=alt2*0.0003048 #ft to km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    d=math.sqrt(d**2+((alt2-alt1)*0.0003048)**2) #in km
    return d
def col_det(plane_name):
    try:
        cred = credentials.Certificate(r"C:\Users\Rimsha khan\Desktop\fire-base\assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
    except:
        pass
    
    database=db.reference("aircraft//data/")
    data=database.get()
    data_json = json.loads(data)
    data=pd.DataFrame(data_json)
    
    check_for=plane_name 
    #Processing

    datacopy=data.copy()
    lowest_Alt=29000
    vertical_separation_below=1000
    vertical_separation_above=2000
    horizontal_separation=18.52
    angle_margin=45
    datacopy=datacopy.drop(data.loc[data["Id"]==check_for].index)
    origin=data.loc[data["Id"]==check_for,["Lat","Long"]]
    origin=list(origin.to_records(index=False))[0]
    Alt_check=data.loc[data["Id"]==check_for,"Alt"]
    Alt_check=Alt_check.values[0]
    angle_check=data.loc[data["Id"]==check_for,"Trak"]
    angle_check=angle_check.values[0]
    speed_check=data.loc[data["Id"]==check_for,"Spd"]
    speed_check=speed_check.values[0]
    lat_check=data.loc[data["Id"]==check_for,"Lat"]
    lat_check=lat_check.values[0]
    long_check=data.loc[data["Id"]==check_for,"Long"]
    long_check=long_check.values[0]
    datacopy['Probability']=0
    datacopy['ETC']="-"
    #seond try
    for index,row in datacopy.iterrows():
        datacopy.loc[index,"Distance_2d"]=distance(origin,(datacopy.loc[index,"Lat"],datacopy.loc[index,"Long"]))
        datacopy.loc[index,"Distance_3d"]=distance_3d(origin,(datacopy.loc[index,"Lat"],datacopy.loc[index,"Long"]),Alt_check,datacopy.loc[index,"Alt"])
        datacopy.loc[index,"Alt_diff"]=Alt_check-datacopy.loc[index,"Alt"] #- if above + if below
        diff=datacopy.loc[index,"Trak"]-angle_check #- if above + if below
        datacopy.loc[index,"angle_diff"]=(diff + 180) % 360 - 180
        if datacopy.loc[index,"Alt_diff"]<0:
            datacopy.loc[index,"Vertical_Position"]="Above"
        elif datacopy.loc[index,"Alt_diff"]>0:
            datacopy.loc[index,"Vertical_Position"]="Below"
        else:
            datacopy.loc[index,"Vertical_Position"]="Same"
        datacopy.loc[index,"Alt_diff"]=abs(datacopy.loc[index,"Alt_diff"])


        if long_check<datacopy.loc[index,"Long"] and lat_check<datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Right, Front"
        elif long_check<datacopy.loc[index,"Long"] and lat_check>datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Right, Back"
        elif long_check>datacopy.loc[index,"Long"] and lat_check>datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Left, Back"
        elif long_check>datacopy.loc[index,"Long"] and lat_check<datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Left, Front"
        elif long_check==datacopy.loc[index,"Long"] and lat_check<datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Front"
        elif long_check==datacopy.loc[index,"Long"] and lat_check>datacopy.loc[index,"Lat"]:
            datacopy.loc[index,"Horizontal_Position"]="Back"
        elif long_check<datacopy.loc[index,"Long"] and lat_check==datacopy.loc[index,"Lat"]:
            datacopy.loc[index,"Horizontal_Position"]="Right"
        elif long_check>datacopy.loc[index,"Long"] and lat_check==datacopy.loc[index,"Lat"]: 
            datacopy.loc[index,"Horizontal_Position"]="Left"
        else:
            datacopy.loc[index,"Horizontal_Position"]="Same"
            
        if datacopy.loc[index,"Alt"]<=lowest_Alt:
            if datacopy.loc[index,"Alt_diff"]<=vertical_separation_below and datacopy.loc[index,"Distance_2d"]<=horizontal_separation:
                datacopy.loc[index,"Status"]="Danger"
                if datacopy.loc[index,"Distance_3d"]<=5: #check if already closest
                    datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0))/3
                    datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check<=datacopy.loc[index,"Long"] and lat_check<=datacopy.loc[index,"Lat"]: #1st quadrant
                    if angle_check>=0 and angle_check<=90: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check<=datacopy.loc[index,"Long"] and lat_check>=datacopy.loc[index,"Lat"]: #2nd quadrant
                    if angle_check>=90 and angle_check<=180: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check>=datacopy.loc[index,"Long"] and lat_check>=datacopy.loc[index,"Lat"]: # 3rd quadrant
                    if angle_check>=180 and angle_check<=270: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check>=datacopy.loc[index,"Long"] and lat_check<=datacopy.loc[index,"Lat"]: #4th quadrant
                    if angle_check>=270 and angle_check<=360: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_below)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])


            else:
                datacopy.loc[index,"Status"]="Safe"
        else:
            if datacopy.loc[index,"Alt_diff"]<=vertical_separation_above and datacopy.loc[index,"Distance_2d"]<=horizontal_separation:
                datacopy.loc[index,"Status"]="Danger"
                if datacopy.loc[index,"Distance_3d"]<=5: #check if already closest
                    datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0))/3
                    datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check<=datacopy.loc[index,"Long"] and lat_check<=datacopy.loc[index,"Lat"]: #1st quadrant
                    if angle_check>=0 and angle_check<=90: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check<=datacopy.loc[index,"Long"] and lat_check>=datacopy.loc[index,"Lat"]: #2nd quadrant
                    if angle_check>=90 and angle_check<=180: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check>=datacopy.loc[index,"Long"] and lat_check>=datacopy.loc[index,"Lat"]: # 3rd quadrant
                    if angle_check>=180 and angle_check<=270: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETA"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])

                elif long_check>=datacopy.loc[index,"Long"] and lat_check<=datacopy.loc[index,"Lat"]: #4th quadrant
                    if angle_check>=270 and angle_check<=360: 
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.8))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])
                    else:
                        datacopy.loc[index,"Probability"]=1-(((abs(datacopy.loc[index,"Alt_diff"])/vertical_separation_above)+(datacopy.loc[index,"Distance_2d"]/horizontal_separation)+0.6))/3
                        datacopy.loc[index,"ETC"]=datacopy.loc[index,"Distance_3d"]/(speed_check+ datacopy.loc[index,"Spd"])


            else:
                datacopy.loc[index,"Status"]="Safe"

    # result=datacopy.loc[datacopy["Status"]=="Danger"]
    # result.reset_index(inplace=True)
    # result.drop("index",axis=1,inplace=True)
    # result
    del datacopy["Distance_3d"]
    del datacopy["angle_diff"]
    datacopy.columns=["Id","Datetime","Latitude","Longitude","Altitude","Speed","Angle","Probability","ETC","Horizontal_Separation","Vertical_Separation","Vertical_Position","Horizontal_Position","Status"]
    center_lat=origin[0]
    center_long=origin[1]
    center_co=[center_lat,center_long]   

    center_info={'Id':plane_name , 'Datetime':0, 'Latitude':center_lat, 'Longitude':center_long, 'Altitude':Alt_check, 'Speed':speed_check, 'Angle':angle_check,
       'Horizontal_Separation':0, 'Vertical_Separation':0, 'Vertical_Position':'A',
       'Horizontal_Position':"R", 'Status':'Safe', 'Probability':0, 'ETC':0}
    datacopy=datacopy.append(center_info,ignore_index=True)
    datacopy=datacopy.fillna(0)
    return ({'data':datacopy,'center':center_co})
def rev_geocoding(lat,long):
    location = geolocator.reverse(str(lat)+", "+str(long))
    return location.address
def live_data(veh,typpe):
    time.sleep(0.5)
    APIKEY=["141121.N6hQcajR5XAwbq","134290.YYwA7u6Ukgnzhn","133560.vm6ZT5uyI93BgXe"]
    api_key=random.choice(APIKEY)
    API="https://api.aprs.fi/api/get?name="+veh+"&what=loc&apikey="+api_key+"&format=json"
    response=requests.get(API)
    status=response.status_code
    entry=(response.json())['entries']
    entry[0]["vehicle_type"]=typpe
    print(f"{veh}-----------{status}")
    return entry[0]  
    
def firebase_location():
    database=firebase.FirebaseApplication("https://assetdata-5e192.firebaseio.com/",None)
    try:
        cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/",
                                       'storageBucket': 'assetdata-5e192.appspot.com'})
    except:
        pass
    database=db.reference("livedata/")
    d=database.get()
    data_json = json.loads(d)
    my_data=pd.DataFrame(data_json)
    url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
    
    m = folium.Map(location=[20, 0], tiles=url,attr='Current Location',zoom_start=2)
    for i in range(0,len(my_data)):
        if my_data.iloc[i]['vehicle_type'].lower()=='truck':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/truck.png',icon_size=(25,25))
        if my_data.iloc[i]['vehicle_type'].lower()=='car':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/car-icon.png',icon_size=(25,25))
        folium.Marker([my_data.iloc[i][2], my_data.iloc[i][3]], popup="ID: "+my_data.iloc[i][0]+"TIME: "+my_data.iloc[i][1],icon=logo_icon).add_to(m),
    m=m._repr_html_()
    return (m)
def current_location():
    database=firebase.FirebaseApplication("https://assetdata-5e192.firebaseio.com/",None)
    try:
        cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/",
                                       'storageBucket': 'assetdata-5e192.appspot.com'})
    except:
        pass 
    #live API
    data_list=[]
    try:
        for typpe,assets in vehicle_names.items():
            for veh in assets:
                data_list.append(live_data(veh,typpe))
        print("SUCCESSFULLY RETRIEVED FROM API")
        my_data=pd.DataFrame(data_list)
        my_data=my_data.loc[:,["name","time","lat","lng","vehicle_type"]]
        my_data["time"]=my_data["time"].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
        data_json=my_data.to_json()
        database=db.reference()
        upload=database.child("livedata/")
        upload.set(data_json)
        print("SUCESSFULY UPLOADED")
        #map
        url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
        
        m = folium.Map(location=[20, 0], tiles=url,attr='Current Location',zoom_start=2)
        for i in range(0,len(my_data)):
            if my_data.iloc[i]['vehicle_type'].lower()=='truck':
                logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/truck.png',icon_size=(25,25))
            if my_data.iloc[i]['vehicle_type'].lower()=='car':
                logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/car-icon.png',icon_size=(25,25))
            folium.Marker([my_data.iloc[i][2], my_data.iloc[i][3]], popup="ID: "+my_data.iloc[i][0]+"TIME: "+my_data.iloc[i][1],icon=logo_icon).add_to(m),
        m=m._repr_html_() #updated
        return(m)
    except:
        print("limit Exceed")
        firebase_location()
        
    
def plane_drop():
    try:
        cred = credentials.Certificate(r"C:\Users\Rimsha khan\Desktop\fire-base\assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
    except:
        pass
    database=db.reference("aircraft//data/")
    data=database.get()
    data_json = json.loads(data)
    data=pd.DataFrame(data_json)
    return(data['Id'].values.tolist())
def vehicle_drop(select):
    return(vehicle_names[select])

def get_data(type_,select,date):
    database=firebase.FirebaseApplication("https://assetdata-5e192.firebaseio.com/",None)
    try:
        cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/",
                                       'storageBucket': 'assetdata-5e192.appspot.com'})
    except:
        pass
        
    bucket = storage.bucket('assetdata-5e192.appspot.com')
  
    url=type_+"/"+select+"/data/"
    blob = bucket.blob(url)
    d=blob.download_as_string()
    s=str(d,'utf-8')
    data = StringIO(s) 
    data=pd.read_csv(data)
   
    
    if date['end_date'] is not None and date['start_date'] is  None:
        data=data.tail(29)
        print('start none')
    else:
        if  date['start_date'] == date['end_date']:
            data[data['DATE']==date['start_date']]
        elif date['start_date'] < date['end_date']:
            mask = (data['DATE'] >= date['start_date']) & (data['DATE'] <= date['end_date'])
        else:
            mask = (data['DATE'] >= date['end_date']) & (data['DATE'] <= date['start_date'])
        data = data.loc[mask]
    
    
      
        
    
        
    #file=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')
    return (data)

def fetch_insight(type_,name,insight):
    try:
        cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
    except:
        pass
    database=db.reference(type_.lower()+"/"+name+"/insights/"+insight+"/")
    d=database.get()
    if insight=='peak_speed':
        speed=d["speed_max"]
        return (speed)
    else:
        data_json = json.loads(d)
        my_data=pd.DataFrame(data_json)
        return my_data

