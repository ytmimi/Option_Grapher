import os
import sys
#adds the app directory to the path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)
from django.test import SimpleTestCase, Client
from django.urls import reverse
import datetime as dt
import random
import views
import forms


class Test_Option_Input_View(SimpleTestCase):
	
	def setUp(self):
		self.client = Client()
		self.valid_input = {
		'position':random.choice(['Long', 'Short']),
		'option_type':random.choice(['Call', 'Put']),
		'strike_price':50,
		'stock_price':50,
		'traded_price':2.14,
		'interest_rate':.012,
		'exp_date':dt.date.today()+dt.timedelta(days=30),
		}

	def test_option_input_get(self):
		url = reverse('options:form')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		

	def test_option_input_post(self):
		url = reverse('options:form')
		response = self.client.post(url, self.valid_input, follow=True)
		self.assertEqual(response.status_code, 200)



