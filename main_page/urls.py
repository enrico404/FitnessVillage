# controller applicazione main_page
from django.urls import path
from . import views

app_name = 'main_page'

urlpatterns = [
    path('', views.welcome, name='welcome'),

]