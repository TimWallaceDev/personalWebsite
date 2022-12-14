from django.test import TestCase, SimpleTestCase

# Create your tests here.

class TestWebsite(SimpleTestCase):

    def testAssertion(self):
        assert 1 + 1 == 2