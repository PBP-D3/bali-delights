from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
# Create your views here.
def show_reviews(request):
    # reviews = Review.objects.all() kalo mau cek semua review
    reviews = Review.objects.filter(user_id=request.user.id)
    context = {
        'reviews' : reviews,
    }

    return render(request, "reviews.html", context)

@login_required
def create_review(request, product_id):
    form = ReviewForm(request.POST or None)
    product = get_object_or_404(Product, id=product_id)

    if (request.method == 'POST'):
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user_id = request.user
            new_review.product_id = product
            new_review.save()


            return redirect('reviews:product_reviews', product_id=product.id)
    else:
        form = ReviewForm()

    context = {'form': form,
               'product': product
               }
    return render(request, "create_review.html", context)

def edit_review(request):
    context = []
    return render(request, "create_review.html", context)


def product_reviews(request, product_id):
    # Fetch product and related reviews
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product_id=product_id)  # Assuming related_name='reviews' in the Review model

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'product_reviews.html', context)

def show_xml(request, product_id):
    data = Review.objects.filter(product_id=product_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/json")

def show_json(request, product_id):
    data = Review.objects.filter(product_id=product_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def user_reviews(request):
    user_reviews = Review.objects.filter(user_id=request.user).select_related('product_id')
    
    context = {
        'user_reviews': user_reviews,
    }
    return render(request, 'user_reviews.html', context)
