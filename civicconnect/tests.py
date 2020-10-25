import requests
from django.test import TestCase

from civic14.settings import API_KEY
from civicconnect.models import Representative

'''
dummy test for travis-CI setup
From Mark Sheriff StaffTextbookExchange-f20
'''
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)


class RepresentativeTest(TestCase):

    def test_create_representative(self):
        name = 'Kanye West'
        party = 'Idiot Party'
        phone = '555-555-5555'
        address = '123 DumbDumb Drive, Calabassas, CA'
        darkest_timeline = Representative(name=name, party=party, phone=phone, address=address)
        darkest_timeline.save()
        self.assertEqual(darkest_timeline.name, Representative.objects.get(name=name).name)
        self.assertEqual(darkest_timeline.party, Representative.objects.get(party=party).party)
        self.assertEqual(darkest_timeline.phone, Representative.objects.get(phone=phone).phone)
        self.assertEqual(darkest_timeline.address, Representative.objects.get(address=address).address)


class CivicInfoApiTests(TestCase):
    civic = 'https://civicinfo.googleapis.com/civicinfo/v2/representatives?address='
    offices = '&includeOffices=true&roles=legislatorUpperBody&roles=legislatorLowerBody&key='

    def test_civic_info_api_zip(self, c=civic, o=offices):
        address = "22903"
        url = c + address + o + API_KEY
        response = requests.get(url)
        data = response.json()
        self.assertEqual('Tim Kaine', data['officials'][0]['name'])

    def test_civic_info_api_address(self, c=civic, o=offices):
        address = "85 Engineer's Way, Charlottesville, VA 22903"
        url = c + address + o + API_KEY
        response = requests.get(url)
        data = response.json()
        self.assertEqual('Denver Riggleman', data['officials'][2]['name'])
