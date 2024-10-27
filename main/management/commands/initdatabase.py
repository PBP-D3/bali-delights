from django.core.management import BaseCommand, call_command
from main.models import User
from products.models import Product
from stores.models import Store
from reviews.models import Review, Like
from carts.models import Cart, CartItem

class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        # Load initial users
        self.load_users()

        # Load initial stores before products
        self.load_stores()

        # Load initial products
        self.load_products()
        
        self.load_reviews()
        
        self.load_carts()
    

    def load_users(self):
        call_command('loaddata', 'initial_users')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

    def load_stores(self):
        call_command('loaddata', 'initial_stores')  # Ensure you have this fixture
        # You don't need to iterate and save stores again after loading
        # unless you need to update any fields.

    def load_products(self):
        call_command('loaddata', 'initial_products')
        
        # If you need to modify any fields after loading, do it here
        for product in Product.objects.all():
            # For example, if you need to ensure product fields are not null
            product.save()  # Save again if you've modified anything
    
    def load_reviews(self):
        call_command('loaddata', 'initial_reviews')
         # If you need to modify any fields after loading, do it here
        for review in Review.objects.all():
            # For example, if you need to ensure product fields are not null
            review.save()  # Save again if you've modified anything
        for like in Like.objects.all():
            # For example, if you need to ensure product fields are not null
            like.save()  # Save again if you've modified anything
            
    def load_carts(self):
        call_command('loaddata', 'initial_reviews')
         # If you need to modify any fields after loading, do it here
        for cart in Cart.objects.all():
            # For example, if you need to ensure product fields are not null
            cart.save()  # Save again if you've modified anything
        for cartitem in CartItem.objects.all():
            # For example, if you need to ensure product fields are not null
            cartitem.save()  # Save again if you've modified anything
        
        
        