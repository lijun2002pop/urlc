from django.contrib import admin
from django.urls import path

from home import views

urlpatterns = [
    path('',views.home),
    path('hi/',views.Test.as_view()),
    path('music/',views.Music_worlds.as_view()),
    path('play/',views.play),
    path('music_list/',views.Music_list.as_view()),
]
