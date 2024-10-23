from django.urls import path
from main.views import show_main
from main.views import register, login_user, logout_user


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    
    path('register', register, name='register'),
    
    path('login', login_user, name='login'),
    
    path('logout', logout_user, name='logout'),  
    
]