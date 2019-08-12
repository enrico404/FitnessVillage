from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'courseManager'
urlpatterns = [
    path('<nomeCorso>/', views.courseDetail, name='courseDetail'),

]