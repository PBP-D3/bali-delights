from django.test import TestCase
from django.urls import reverse
from main.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Store
from products.models import Product

class StoreViewTests(TestCase):
    def setUp(self):
        # Create a shop owner user
        self.shop_owner = User.objects.create_user(
            username='shopowner',
            password='password123',
            role='shop_owner'
        )
        # Create a normal user
        self.normal_user = User.objects.create_user(
            username='normaluser',
            password='password123',
            role='normal_user'
        )
        # Create a store owned by the shop owner
        self.store = Store.objects.create(
            owner_id=self.shop_owner,
            name="Test Store",
            description="A test store",
            photo="https://example.com/image.jpg",
            location="Test Location"
        )
        # URL paths
        self.owner_store_url = reverse('stores:owner_store_view', args=[self.store.id])
        self.edit_store_url = reverse('stores:edit_store', args=[self.store.id])

    def test_owner_store_view_access_by_owner(self):
        # Log in as the store owner
        self.client.login(username='shopowner', password='password123')
        response = self.client.get(self.owner_store_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Store")
    
    def test_owner_store_view_access_denied_for_normal_user(self):
        # Log in as a normal user
        self.client.login(username='normaluser', password='password123')
        response = self.client.get(self.owner_store_url)
        self.assertEqual(response.status_code, 403)  # Expect Forbidden for non-owners
    
    def test_edit_store_view_get_accessible_by_owner(self):
        # Log in as the store owner
        self.client.login(username='shopowner', password='password123')
        response = self.client.get(self.edit_store_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Your Store")
    
    def test_edit_store_view_post_updates_store(self):
        # Log in as the store owner
        self.client.login(username='shopowner', password='password123')
        data = {
            'name': 'Updated Store Name',
            'description': 'Updated Description',
            'location': 'Updated Location',
            'choice': 'url',
            'photo': 'https://example.com/updated_image.jpg'
        }
        response = self.client.post(self.edit_store_url, data)
        self.store.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Expect a redirect after successful update
        self.assertEqual(self.store.name, 'Updated Store Name')
        self.assertEqual(self.store.description, 'Updated Description')
        self.assertEqual(self.store.location, 'Updated Location')
        self.assertEqual(self.store.photo, 'https://example.com/updated_image.jpg')
    
    def test_edit_store_view_access_denied_for_normal_user(self):
        # Log in as a normal user
        self.client.login(username='normaluser', password='password123')
        response = self.client.get(self.edit_store_url)
        self.assertEqual(response.status_code, 403)  # Expect Forbidden for non-owners

    def test_delete_store_accessible_by_owner(self):
        # Log in as the store owner
        self.client.login(username='shopowner', password='password123')
        response = self.client.post(reverse('stores:delete_store', args=[self.store.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Store.objects.filter(id=self.store.id).exists())
    
    def test_delete_store_access_denied_for_normal_user(self):
        # Log in as a normal user
        self.client.login(username='normaluser', password='password123')
        response = self.client.post(reverse('stores:delete_store', args=[self.store.id]))
        self.assertEqual(response.status_code, 403)  # Expect Forbidden for non-owners
        self.assertTrue(Store.objects.filter(id=self.store.id).exists())  # Store should still exist

class UserModelTests(TestCase):
    def test_user_is_shop_owner(self):
        user = User.objects.create_user(
            username='shopowner',
            password='password123',
            role='shop_owner'
        )
        self.assertTrue(user.is_admin())
    
    def test_user_is_not_shop_owner(self):
        user = User.objects.create_user(
            username='normaluser',
            password='password123',
            role='normal_user'
        )
        self.assertFalse(user.is_admin())
