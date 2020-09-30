from django.urls import path
from . import views
from tracking.dash_apps.finished_apps import simpleexample ,mostly_taken_route,bar_chart,history,mostly_visited_location,hour_gauge,most_active_hours,highest_speed_gauge,fuel_week,fuel_date,avg_activehour_date,avg_activehour_week,density_heat_map,avg_distance

urlpatterns = [
path('tracking/',views.tracking,name='tracking'),
#path('tracking/my_page/',views.my_page,name='my_page'),
path('tracking/insights/',views.insights,name='insights'),
path('tracking/collision_detection/',views.collision_detection,name='collision_detection'),
path('tracking/vehicle_history/',views.veh_hist,name='vehicle_history'), 
path('',views.login,name="login"),
path('logout/',views.logout,name="logout"),
]