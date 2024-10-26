from django.urls import path
from reviews.views import show_reviews, create_review, edit_review, product_reviews, show_xml, show_json, user_reviews

app_name = 'reviews'

urlpatterns = [
    path('', show_reviews, name='show_reviews'),
    # path('create-review', create_review, name='create_review'),
    path('edit-review/<int:review_id>', edit_review, name='edit_review'),
    # path('delete-review/<int:review_id>', delete_review, name='delete_review')
    path('<int:product_id>', product_reviews, name='product_reviews'),
    path('<int:product_id>/create-review/', create_review, name='create_review'),
    # path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
    # path('product/<int:product_id>/create_review/', create_review, name='create_review'),
    path('<int:product_id>/xml', show_xml, name = 'show_xml'),
    path('<int:product_id>/json', show_json, name = 'show_json'),
    path('my-review/', user_reviews, name='user_reviews'),

]

