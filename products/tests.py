from django.test import TestCase
from django.urls import reverse
from .models import Product, Store

# class ProductTestCase(TestCase):
#     def setUp(self):
#         self.store = Store.objects.create(name="Test Store")
        
#         # Create a couple of products for testing
#         Product.objects.create(
#             name="Test Product 1",
#             description="Description for product 1",
#             price=10.99,
#             stock=100,
#             store=self.store
#         )
#         Product.objects.create(
#             name="Test Product 2",
#             description="Description for product 2",
#             price=20.99,
#             stock=50,
#             store=self.store
#         )

#     def test_show_products_view(self):
#         # Get the URL for the product list view
#         url = reverse('products:show_products')
        
#         # Make a GET request to the view
#         response = self.client.get(url)
        
#         # Ensure the view returns a 200 OK status
#         self.assertEqual(response.status_code, 200)
        
#         # Check if the products are in the context of the response
#         products = response.context['products']
#         self.assertEqual(len(products), 2)
#         self.assertEqual(products[0].name, "Test Product 1")
#         self.assertEqual(products[1].name, "Test Product 2")

