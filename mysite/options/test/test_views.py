import os
import sys
#adds the app directory to the path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)
from django.test import TestCase, Client
from django.urls import reverse
import datetime as dt
import random
import views
import forms


class Test_Option_Input_View(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.valid_input = {
		'quantity':1,
		'position':random.choice(['Long', 'Short']),
		'option_type':random.choice(['Call', 'Put']),
		'strike_price':50,
		'stock_price':50,
		'traded_price':2.14,
		'interest_rate':.012,
		'exp_date':dt.date.today()+dt.timedelta(days=30),
		}
		self.url = reverse('options:form')
		self.get_response = self.client.get(self.url)
		self.post_response = self.client.post(self.url, self.valid_input)

	def test_option_input_get(self):
		self.assertEqual(self.get_response.status_code, 200)
	
	def test_correct_template_get(self):
		self.assertTemplateUsed(self.get_response, 'options/options_forms.html')

	def test_option_input_post(self):
		self.assertEqual(self.post_response.status_code, 200)

	def test_correct_template_push(self):
		self.assertTemplateUsed(self.post_response, 'options/options_forms.html')



