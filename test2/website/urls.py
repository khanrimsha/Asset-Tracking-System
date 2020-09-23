from django.urls import path
from . import views

urlpatterns = [

  
  

 path('maps/',views.folium_map,name="maps"),

 
]
