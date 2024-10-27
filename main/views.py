from django.shortcuts import render, redirect, reverse   # Tambahkan import redirect di baris ini
from django.http import HttpResponse
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
from django.utils.html import strip_tags
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

