from django.test import TestCase

# Create your tests here.

'''
dummy test for travis-CI setup
From Mark Sheriff StaffTextbookExchange-f20
'''
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)
        