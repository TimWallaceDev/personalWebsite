from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name="index"),
    path('samplelist', views.samplelist),
    path('keywordadmin', views.admin, name='admin'),
    path('about', views.about),
    path('topwords', views.topwords),
    path('33', views.thirtythree),
]