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
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as auth_logout

from main.models import User  # Import custom User model 

@csrf_exempt
def LoginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt 
def RegisterView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            password_confirm = data.get('password_confirm')
            
            # Validate required fields
            if not all([username, password, password_confirm]):
                return JsonResponse({
                    'status': False,
                    'message': 'All fields are required'
                }, status=400)
            
            # Check password match
            if password != password_confirm:
                return JsonResponse({
                    'status': False, 
                    'message': 'Passwords do not match'
                }, status=400)
            
            # Check username availability
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': False,
                    'message': 'Username already exists'
                }, status=400)
            
            # Create user with custom model
            user = User.objects.create_user(
                username=username,
                password=password,
                money=0  # Set initial money value
            )
            
            return JsonResponse({
                'status': True,
                'message': 'Registration successful',
                'user': {
                    'username': user.username,
                    'id': user.id,
                    'money': user.money
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': False,
                'message': 'Invalid JSON data'
            }, status=400)
            
    return JsonResponse({
        'status': False,
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
def LogoutView(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)