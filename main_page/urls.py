# controller applicazione main_page
from django.urls import path
from . import views

app_name = 'main_page'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('corso/<nomeCorso>', views.corso, name='corso'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('login/', views.login, name='login'),
    path('registrati/', views.registrati, name='registrati'),
    path('assistenza/', views.assistenza, name='assistenza'),
    path('messaggi/', views.messaggi, name='messaggi'),
    path('rispondi/<messageID>', views.rispondi, name='rispondi'),

]