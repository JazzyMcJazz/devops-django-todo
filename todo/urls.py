from django.urls import path
from todo import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todos, name='todos'),
    path('todos/<int:pk>/', views.todos, name='todos_pk'),
    path('todos/<int:pk>/edit-form/', views.todos_edit_form, name='todos_edit_form'),
]
