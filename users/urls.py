from django.urls import path
from .views import login_point, register

urlpatterns = [

    path('login/', login_point, name='login'),
    path('register/', register, name='register'),

]
