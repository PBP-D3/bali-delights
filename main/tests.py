from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.utils import timezone
# from .models import MoodEntry

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/skibidi/')
        self.assertEqual(response.status_code, 404)

    # def test_strong_mood_user(self):
    #     now = timezone.now()
    #     mood = MoodEntry.objects.create(
    #       mood="LUMAYAN SENANG",
    #       time = now,
    #       feelings = "senang sih, cuman tadi baju aku basah kena hujan :(",
    #       mood_intensity = 8,
    #     )
    #     self.assertTrue(mood.is_mood_strong)
