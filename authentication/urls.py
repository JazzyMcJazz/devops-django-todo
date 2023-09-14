from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('accounts/register', views.register, name='register'),
]
