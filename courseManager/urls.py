from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'courseManager'
urlpatterns = [
    path('<nomeCorso>/', views.courseDetail, name='courseDetail'),
    path('<int:corsoID>/prenotazione', views.prenotazione, name='prenotazione'),
    path('<str:nomeCorso>/insertCourse', views.insert, name='insert'),
    path('<int:corsoID>/cancella', views.cancella, name='cancella'),
]