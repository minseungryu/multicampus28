# -*- coding:utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),                        # views.py 파일에서 index 함수를 찾아!
    path('createTodo', views.createTodo, name= "createTodo"),   # index.html from 태그의 action과 연결되어 있음
    path('deleteTodo/', views.deleteTodo, name= "deleteTodo")
]