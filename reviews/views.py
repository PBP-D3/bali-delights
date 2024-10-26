from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from products.models import Product
# Create your views here.
# Create your views here.
def show_reviews(request):
    # reviews = Review.objects.all() kalo mau cek semua review
    reviews = Review.objects.filter(user=request.user)
    context = {
        'reviews' : reviews,
    }

    return render(request, "reviews.html", context)

def create_review(request):
    form = ReviewForm(request.POST or None)

    if (request.method == 'POST'):
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            # ID PLACEHOLDER GANTI SAMA YG BENER
            new_review.product = Product.objects.filter(id=1)
            return redirect('main:show_main')
    else:
        form = ReviewForm()

    context = {'form': form}
    return render(request, "add_review.html", context)

def edit_review(request):
    context = []
    return render(request, "add_review.html", context)
