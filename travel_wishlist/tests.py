from re import T
from django.test import TestCase
from django.urls import reverse

from .models import Place
# Create your tests here.
#unit tests check code logic, not imitate user
class TestHomePage(TestCase):
    #don't forget argument self
    def test_home_page_shows_empty_list_for_empty_db(self):
        home_page_url=reverse('place_list')
        response = self.client.get(home_page_url)
        #client can make get and post requests
        #making assertions about the response
        #django will make a temp db, every test begins with a new db
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

    #test fixtures -- preloaded data before test start running

class TestWishlist(TestCase):
    fixtures=['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response= self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestNoPlacesVisited(TestCase):
    def test_no_places_visited_message(self):
        response=self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response,'You have not visited any places on your list yet.')

class visitedList(TestCase):
    fixtures=['test_places']
    def test_visited_list_has_visited_palces(self):
        response=self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class testAddNewPlace(TestCase):
    def test_add_new_univisted_place(self):
        add_place_url = reverse('place_list')
        new_place_data={'name':'Tokyo','visited':False}

        response = self.client.post(add_place_url,new_place_data, follow = True)
        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html')
        response_places = response.context['places']
        #see places
        self.assertEqual(1,len(response_places)) 
        tokyo_template = response_places[0]
        tokyo_db = Place.objects.get(name = 'Tokyo', visited = False)
        self.assertEqual(tokyo_db,tokyo_template)

class TestVisitPlaces(TestCase):
    fixtures = ['test_places']
    def test_visit_new_place(self):
        visit_place_url = reverse('place_was_visited', args = (2,))
        response = self.client.post(visit_place_url,follow = True)

        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')
        #open the db
        new_york = Place.objects.get(pk = 2)
        self.assertTrue(new_york.visited)

    def test_place_does_not_exist(self):
        visit_place_doesnt_exist_url = reverse('place_was_visited', args = (123456, ))
        response = self.client.post(visit_place_doesnt_exist_url,follow=True)
        self.assertEqual(404,response.status_code)