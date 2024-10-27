from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Chat, Message
from stores.models import Store

User = get_user_model()

class ChatTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.shop_owner = User.objects.create_user(username="shopowner", password="password123", role="shop_owner")

        self.store = Store.objects.create(
            name="Test Store",
            location="Test Location",
            description="A test store",
            photo="https://example.com/photo.jpg",
            owner_id=self.shop_owner
        )

        self.client = Client()
        self.client.login(username="testuser", password="password123")

    def test_create_chat(self):
        response = self.client.post(reverse("create_chat"), {"store_id": self.store.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Chat.objects.filter(sender=self.user, store=self.store).exists())
        self.assertEqual(response.json().get("success"), True)

    def test_list_chats_view(self):
        Chat.objects.create(sender=self.user, store=self.store)
        response = self.client.get(reverse("list_chats"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Store")

    def test_send_message(self):
        chat = Chat.objects.create(sender=self.user, store=self.store)
        response = self.client.post(reverse("send_message", args=[chat.id]), {"message": "Hello!"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(chat=chat, content="Hello!").exists())
        self.assertEqual(response.json().get("success"), True)

    def test_edit_message(self):
        chat = Chat.objects.create(sender=self.user, store=self.store)
        message = Message.objects.create(chat=chat, sender=self.user, content="Original Message")

        response = self.client.post(reverse("edit_message", args=[message.id]), {"content": "Edited Message"})
        self.assertEqual(response.status_code, 200)
        message.refresh_from_db()
        self.assertEqual(message.content, "Edited Message")

    def test_delete_chat(self):
        chat = Chat.objects.create(sender=self.user, store=self.store)
        response = self.client.post(reverse("delete_chat", args=[chat.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Chat.objects.filter(id=chat.id).exists())
        self.assertEqual(response.json().get("success"), True)

    def tearDown(self):
        User.objects.all().delete()
        Store.objects.all().delete()
        Chat.objects.all().delete()
        Message.objects.all().delete()