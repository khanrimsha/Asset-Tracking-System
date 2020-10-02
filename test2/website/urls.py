from django.urls import path
from . import views

urlpatterns = [

  
  
path('route/',views.route_map,name="route"),
 path('maps/',views.folium_map,name="maps"),

 
]
