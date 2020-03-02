from django.urls import path     
from . import views
urlpatterns = [
    path('', views.homepage),
    path('register', views.register_page),
    path('login', views.login_page),
    path('register/process', views.register),
    path('login/process', views.login),
    path('dashboard', views.dashboard),	 
    path('logout', views.logout),
    path('trip/add', views.add_trip_page),
    path('add_trip', views.add_trip),  
    path('trip/edit/<int:num>', views.edit_trip_page),
    path('trip/edit/<int:num>/process', views.edit_trip),
    path('trip/<int:num>', views.trip_info_page),
    path('delete/<int:num>', views.delete_trip)
]