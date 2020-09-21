from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample,bar_chart

urlpatterns = [
path('home/',views.home,name='home'),
   
]