from django.urls import path
from main.views import show_main, register, login_user, logout_user, top_reviews_json
from main.views import LoginView, LogoutView, RegisterView

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register', register, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('top-reviews-json/', top_reviews_json, name='top_reviews_json'),
    path('api/login/', LoginView, name='api_login'),
    path('api/logout/', LogoutView, name='api_logout'),
        path('api/register/', RegisterView, name='api_register'),
    path('api/top-reviews/', top_reviews_json, name='api_top_reviews')
]