from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Review, Like
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict
from django.db.models import Count

import json
# Create your views here.

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

@csrf_exempt
@login_required
@require_POST
def create_review_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    
    form = ReviewForm(data)
    
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.user_id = request.user
        new_review.product_id = product
        new_review.save()
        
        created_review = model_to_dict(new_review)
        return JsonResponse({'success': True, 'review': created_review}, status=201)
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@csrf_exempt
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user_id=request.user)
    
    if request.method == 'POST':
        # Load JSON data from request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

        # Populate the form with JSON data
        form = ReviewForm(data, instance=review)
        
        if form.is_valid():
            form.save()
            updated_review = model_to_dict(review)
            return JsonResponse({'success': True, 'review': updated_review}, status=200)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    # GET request for pre-filling form data in modal
    elif request.method == 'GET':
        review_data = model_to_dict(review)
        return JsonResponse({'success': True, 'review': review_data}, status=200)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user_id=request.user)
    
    if request.method == 'POST':
        review.delete()
        return JsonResponse({'success': True, 'review_id': review_id}, status=200)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def product_reviews(request, product_id):
    # Fetch product and related reviews
    product = get_object_or_404(Product, id=product_id)
    if (request.user.is_authenticated):
        reviews = Review.objects.filter(product_id=product_id).select_related('user_id')

        # If user authenticated
        for review in reviews:
            # Add a `liked` attribute for each review
            review.liked = review.like_set.filter(user_id=request.user).exists()
        
        user_review_exists = Review.objects.filter(product_id=product_id, user_id=request.user)

        
        context = {
            'product': product,
            'reviews': reviews,
            'user_review_exists': user_review_exists
        }
    else:
        reviews = Review.objects.filter(product_id=product_id)  # Assuming related_name='reviews' in the Review model
        context = {
            'product': product,
            'reviews': reviews,
        }
    
    return render(request, 'product_reviews.html', context)

def show_xml(request, product_id):
    data = Review.objects.filter(product_id=product_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/json")

def show_json(request, product_id):
    data = Review.objects.filter(product_id=product_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def user_reviews(request):
    user_reviews = Review.objects.filter(user_id=request.user).select_related('product_id')
    
    context = {
        'user_reviews': user_reviews,
    }
    return render(request, 'user_reviews.html', context)

@login_required
@csrf_exempt
def toggle_like(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        existing_like = Like.objects.filter(user_id=request.user, review_id=review).first()

        if existing_like:
            # Unlike if the like exists
            existing_like.delete()
            liked = False
        else:
            # Create a like if it doesn't exist
            Like.objects.create(user_id=request.user, review_id=review)
            liked = True

        # Return the total like count and status
        like_count = Like.objects.filter(review_id=review).count()
        return JsonResponse({'liked': liked, 'like_count': like_count}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def product_reviews_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product_id=product_id).select_related('user_id')
    user_review_exists = reviews.filter(user_id=request.user.id).exists() if request.user.is_authenticated else True
    
    reviews_data = [
        {
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "user": {
                "id": review.user_id.id,
                "username": review.user_id.username,
            },
            "product": {
                "id": review.product_id.id,
                "name": review.product_id.name,
                "image": review.product_id.get_image(),
            },
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "total_likes": review.like_set.count(),
            "liked_by_user": review.like_set.filter(user_id=request.user.id).exists() if request.user.is_authenticated else False,
        }
        for review in reviews
    ]
    
    response_data = {
        "product": {
            "id": product.id,
            "name": product.name,
            "image": product.get_image(),
        },
        "reviews": reviews_data,
        "user_review_exists": user_review_exists
    }
    
    return JsonResponse(response_data, safe=False)

@login_required
def user_reviews_json(request):
    user_reviews = Review.objects.filter(user_id=request.user).select_related('product_id')
    user_reviews_data = [
        {
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "user": {
                "id": review.user_id.id,
                "username": review.user_id.username,
            },
            "product": {
                "id": review.product_id.id,
                "name": review.product_id.name,
                "image": review.product_id.get_image(),
            },
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "total_likes": review.like_set.count(),
            "liked_by_user": review.like_set.filter(user_id=request.user.id).exists(),
        }
        for review in user_reviews
    ]
    return JsonResponse(user_reviews_data, safe=False)
