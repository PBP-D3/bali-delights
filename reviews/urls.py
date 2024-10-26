from django.urls import path
from reviews.views import show_reviews, create_review, edit_review

app_name = 'reviews'

urlpatterns = [
    path('', show_reviews, name='show_reviews'),
    path('create-review', create_review, name='create_review'),
    path('edit-review/<int:review_id>', edit_review, name='edit_review'),
    # path('delete-review/<int:review_id>', delete_review, name='delete_review')
]

