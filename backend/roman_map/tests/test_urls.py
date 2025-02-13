from django.test import SimpleTestCase
from django.urls import resolve, reverse

from roman_map import views

class TestUrls(SimpleTestCase):
    def test_getTerritories_url(self):
        url = reverse('getTerritories')
        self.assertEqual(resolve(url).func, views.getTerritories)
    def test_getHistories_url(self):
        url = reverse('getHistories')
        self.assertEqual(resolve(url).func, views.getHistories)
