from django.urls import path
from . import views

urlpatterns = [

   path('index/',views.index,name ="index"),
   path('',views.login,name="login"),
   path('logout/',views.logout,name="logout"),
   path('leaflet/',views.leaf,name="leaf"),
 path('folium_map/',views.folium_map,name="folium_map"),
 path('maps/',views.folium_map,name="maps"),

 
]
