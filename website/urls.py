from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.five, name="index"),
    path('five-about', views.fiveAbout, name="about"),
    path('five-projects', views.fiveProjects, name="projects"),
    path('moreprojects', views.moreprojects, name="moreprojects"),
    path('five-gear', views.fiveGear, name="gear"),
    path('tasks', views.tasks, name="tasks"),
    path('archive', views.archive, name="archive"),
    path('tbonesbikeshop', views.tbonesbikeshop, name="tbonesbikeshop"),
    path('calculator', views.calculator, name="calculator"),
    path('isittoohottowork', views.isittoohottowork, name="isittoohottowork"),
    path('answer', views.answer, name="answer"),
    path('education', views.education, name="education"),
    path('coinsort', views.coinsort, name="coinsort"),
    path('paystoquit', views.paystoquit, name="paystoquit"),
    path('generator/<str:keyword>', views.imageGenerator),
    path('mints', views.mints),
    path('popupdemo', views.popupdemo),
    path('musicquiz', views.musicquiz),
    path('musicquiz2', views.musicquiz2),
    path('blog', views.blog),
    path('blogpost', views.blogpost),
    path('blogsecret', views.blogSecret),
    path('spotipy', views.spotipy1),
    path('lists', views.lists),
    path('listDelete', views.listDelete),
]
