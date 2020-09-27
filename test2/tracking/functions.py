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

vehicle_names={
    'Car':["KC7LZD-9","KI7MH-7","SJ2W-9","SM5RVH-9","VA3MSV-9","VE3TEJ-15"],
    'Truck':['KE4KMD-14','KD5TBX-14','KC0HT-14','N3EOP-14','K7VR-14','N7QIN-14','PD1HPB-14','KN4JUU-14','F4IKQ-9','WB0HBJ-14','SP4XKS-5','KE8WES-14','KE6UWJ-14','KC2HTC-14']

}
car_count=len(vehicle_names['Car'])
truck_count=len(vehicle_names['Truck'])
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
    d=math.sqrt(d**2+(alt2-alt1)**2) #in km
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
    center_df=data[data['Id']==plane_name]#fetching center data
    center_co=center_df.loc[:,['Lat','Long']].values.tolist()    

    center_info={'Id':plane_name , 'Datetime':0, 'Latitude':center_co[0][0], 'Longitude':center_co[0][1], 'Altitude':0, 'Speed':0, 'Angle':0,
       'Horizontal_Separation':0, 'Vertical_Separation':0, 'Vertical_Position':'A',
       'Horizontal_Position':"R", 'Status':'Safe', 'Probability':0, 'ETC':0}
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
    datacopy.columns=["Id","Datetime","Latitude","Longitude","Altitude","Speed","Angle","Horizontal_Separation","Vertical_Separation","Vertical_Position","Horizontal_Position","Status","Probability","ETC"]
    datacopy=datacopy.append(center_info,ignore_index=True)
    datacopy=datacopy.fillna(0)
    return ({'data':datacopy,'center':center_co[0]})

def current_location():
    url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
    my_data=pd.read_csv('D:/django/test2/website/data/point.csv')
    m = folium.Map(location=[20, 0], tiles=url,attr='Current Location',zoom_start=2)
    for i in range(0,len(my_data)):
        if my_data.iloc[i]['type']=='plane':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/my_plane.png',icon_size=(25,25))
        if my_data.iloc[i]['type']=='car':
            logo_icon=folium.features.CustomIcon('D:/django/test2/website/data/car-icon.png',icon_size=(25,25))
        folium.Marker([my_data.iloc[i][1], my_data.iloc[i][2]], popup=my_data.iloc[i][0],icon=logo_icon).add_to(m),
    m=m._repr_html_() #updated
    return(m)
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
def history_map():
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
    return (m2)
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

