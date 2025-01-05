from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("planAi",views.planner,name='planner'),
    path("api/submit_data/",views.submit_data,name="submit_data"),
    path("api/get_itinerary/",views.Get_itinerary,name='get_itinerary'),
]