from selenium.webdriver.firefox.webdriver import WebDriver
#from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):
    @classmethod
    def SetUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_on_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist',self.selenium.title)

class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def SetUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_new_place(self):
        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id-name')
        input_name.send_keys('Madison')

        add_button = self.selenium.find_element_by_id('add_new_place')
        add_button.click()

        madison = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Madison', madison.text)

        self.assertIn('Madison', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)