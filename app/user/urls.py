"""
URL  mapping for the user API.
"""
from django.urls import path

from . import views


app_name = 'user'

urlpatterns = [
    # Token Authentication
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/login/', views.CreateAuthTokenView.as_view(), name='token'),
    path('me/', views.ManageUsersView.as_view(), name='me'),   
    path('token/logout/', views.DestroyAuthTokenView.as_view(), name='logout'),
    
]