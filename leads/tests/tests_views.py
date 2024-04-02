from django.test import TestCase
from django.shortcuts import reverse
class LandingPageTest(TestCase):
    
    def test_status_code(self):
        #TODO some dort of test
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")