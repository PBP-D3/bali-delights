from django.urls import path
from reviews.views import create_review, edit_review, delete_review, product_reviews, show_xml, show_json, user_reviews, toggle_like, product_reviews_json, user_reviews_json, create_review_json

app_name = 'reviews'

urlpatterns = [
    path('edit-review/<int:review_id>', edit_review, name='edit_review'),
    path('<int:product_id>', product_reviews, name='product_reviews'),
    path('<int:product_id>/json', product_reviews_json, name='product_reviews_json'),
    path('<int:product_id>/create-review/', create_review, name='create_review'),
    path('<int:product_id>/xml', show_xml, name = 'show_xml'),
    path('<int:product_id>/json', show_json, name = 'show_json'),
    path('my-review/', user_reviews, name='user_reviews'),
    path('my-review/json', user_reviews_json, name='user_reviews_json'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),
    path('create-review-json/<int:product_id>/', create_review_json, name='create_review_json'),
    path('toggle-like/<int:review_id>/', toggle_like, name='toggle_like'),
]