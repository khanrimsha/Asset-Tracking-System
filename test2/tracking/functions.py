import folium
import numpy
import pandas as pd
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import json
url="car/KC7LZD-9/data/"
vehicle_names={
    'car':["KC7LZD-9","KI7MH-7","SJ2W-9","SM5RVH-9","VA3MSV-9","VE3TEJ-15"],
    'truck':['KE4KMD-14','KD5TBX-14','KC0HT-14','N3EOP-14','K7VR-14','N7QIN-14','PD1HPB-14','KN4JUU-14','F4IKQ-9','WB0HBJ-14','SP4XKS-5','KE8WES-14','KE6UWJ-14','KC2HTC-14']

}
def col_det(plane_name):
    return(pd.read_csv('C:/Users/Rimsha khan/Desktop/most_taken_route.csv'))
def var():
    return(8)
def plane_drop():
    file=pd.read_json('C:/Users/Rimsha khan/Desktop/insights/insights/aircrafts.json')
    return(file['Id'].values.tolist())
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
def history_data():
    try:
        cred = credentials.Certificate(r"C:/Users/Rimsha khan/Desktop/fire-base/assetdata-5e192-firebase-adminsdk-u026s-04925bb72d.json")
        firebase_admin.initialize_app(cred,{"databaseURL":"https://assetdata-5e192.firebaseio.com/"})
    except:
        pass
    database=db.reference(url)
    d=database.get()
    data_json = json.loads(d)
    fuel_used=pd.DataFrame(data_json)
    fuel_used.to_csv('C:/Users/Rimsha khan/Desktop/firedata.csv')
    file=pd.read_csv('C:/Users/Rimsha khan/Desktop/Extra/test/Power BI/truck_structured_data.csv')
    return (fuel_used)

