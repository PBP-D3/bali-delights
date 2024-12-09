from django.shortcuts import render, redirect, reverse   # Tambahkan import redirect di baris ini
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Count
from reviews.models import Review, Like

from django.templatetags.static import static

from .forms import CustomUserCreationForm  # Import your custom form

User = get_user_model()

# Create your views here.
# main/views.py
def show_main(request):
    # Prepare context with user information
        # Fetch top 5 reviews with the highest number of likes
    top_reviews = Review.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:5]
    context = {
        'top_reviews': top_reviews,
    }
    return render(request, "main.html", context)

def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def top_reviews_json(request):
    top_reviews = Review.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:5]
    top_reviews_data = [
        {
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "user": {
                "id": review.user_id.id,
                "username": review.user_id.username,
            },
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "total_likes": review.like_set.count(),
            "liked_by_user": review.like_set.filter(user_id=request.user.id).exists() if request.user.is_authenticated else False,
        }
        for review in top_reviews
    ]
    return JsonResponse(top_reviews_data, safe=False)

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def LoginView(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({
                'status': 'success',
                'message': 'Logged in successfully',
                'user': {
                    'username': user.username,
                    'id': user.id
                }
            })
            response.set_cookie(
                'sessionid',
                request.session.session_key,
                httponly=True,
                samesite='None',
                secure=True
            )
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def LogoutView(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            response = JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
            response.delete_cookie('sessionid')
            return response
        return JsonResponse({'status': 'error', 'message': 'Not logged in'}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def RegisterView(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        password_confirm = body.get('password_confirm')
        
        if password != password_confirm:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def check_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'success',
            'isAuthenticated': True,
            'user': {
                'username': request.user.username,
                'id': request.user.id
            }
        })
    return JsonResponse({
        'status': 'success',
        'isAuthenticated': False
    })