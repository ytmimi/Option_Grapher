import unittest
import os
import sys
#adds the app directory to the path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

import forms
import datetime as dt
from django.test import SimpleTestCase, TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
import random


class Test_Option_Form(SimpleTestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=False)
		self.valid_input = {
		'quantity':1,
		'position':random.choice(['Long', 'Short']),
		'option_type':random.choice(['Call', 'Put']),
		'strike_price':50,
		'stock_price':50,
		'traded_price':2.14,
		'interest_rate':.012,
		'days_till_exp':dt.date.today()+dt.timedelta(days=30),
		}
		self.valid_form = forms.Option_Form(self.valid_input)
		self.invalid_input = {
		'quantity':-1,
		'position':random.choice(['Long', 'Short']),
		'option_type':random.choice(['Call', 'Put']),
		'strike_price':-50,
		'stock_price':-50,
		'traded_price':-2.14,
		'interest_rate':-.012,
		'days_till_exp':dt.date.today()-dt.timedelta(days=30),
		}
		self.invalid_form = forms.Option_Form(self.invalid_input)

	def test_correct_positive_num_inputs(self):
		#the form is created with positive numbers
		self.assertTrue(self.valid_form.is_valid())

	def test_quantity_less_than_1(self):
		self.assertEqual(self.invalid_form.errors['quantity'][0],
			'Must be greater than or equal to 1')

	def test_negative_strike_input(self):
		self.assertEqual(self.invalid_form.errors['strike_price'][0], 
						'Must be greater than or equal to 0.')

	def test_negative_stock_input(self):
		self.assertEqual(self.invalid_form.errors['stock_price'][0], 
						'Must be greater than or equal to 0.')

	def test_negative_price_input(self):
		self.assertEqual(self.invalid_form.errors['traded_price'][0], 
						'Must be greater than or equal to 0.')

	def test_negative_rate_input(self):
		self.assertEqual(self.invalid_form.errors['interest_rate'][0], 
						'Must be greater than or equal to 0.')

	def test_valid_date_format(self):
		date_input_formats=[
			'%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
			'%-m/%d/%Y', '%-m/%d/%y', '%-m-%d-%Y', '%-m-%d-%y',
			'%m/%-d/%Y', '%m/%-d/%y', '%m-%-d-%Y', '%m-%-d-%y',
			'%-m/%-d/%Y', '%-m/%-d/%y', '%-m-%-d-%Y', '%-m-%-d-%y'
		]
		date = self.valid_input['days_till_exp']
		for dt_format in date_input_formats:
			self.valid_input['days_till_exp'] = dt.datetime.strftime(date, dt_format)
			form = forms.Option_Form(self.valid_input)
			self.assertTrue(form.is_valid())

	def test_invalid_date_format(self):
		date_input_formats=['%b, %d, %Y', '%B, %d, %Y']
		date = self.valid_input['days_till_exp']
		for dt_format in date_input_formats:
			self.valid_input['days_till_exp'] = dt.datetime.strftime(date, dt_format)
			form = forms.Option_Form(self.valid_input)
			self.assertEqual(form.errors['days_till_exp'][0], 'Use date format: Month/Day/Year or Month-Day-Year')

	def test_clean_position(self):
		self.valid_form.is_valid()
		if self.valid_input['position'] == 'Long':
			self.assertEqual(self.valid_form.cleaned_data['position'], 1)
		else:
			self.assertEqual(self.valid_form.cleaned_data['position'], -1)


	def test_clean_option_type(self):
		self.valid_form.is_valid()
		self.assertEqual(self.valid_form.cleaned_data['option_type'], 
						self.valid_input['option_type'])

	def test_clean_strike(self):
		self.valid_form.is_valid()
		self.assertEqual(self.valid_form.cleaned_data['strike_price'], 
						self.valid_input['strike_price'])

	def test_clean_stock(self):
		self.valid_form.is_valid()
		self.assertEqual(self.valid_form.cleaned_data['stock_price'], 
						self.valid_input['stock_price'])

	def test_clean_price(self):
		self.valid_form.is_valid()
		self.assertEqual(self.valid_form.cleaned_data['traded_price'], 
						self.valid_input['traded_price'])

	def test_clean_interest_rate(self):
		self.valid_form.is_valid()
		self.assertEqual(self.valid_form.cleaned_data['interest_rate'], 
						self.valid_input['interest_rate'])

	def test_clean_exp_date(self):
		self.valid_form.is_valid()
		self.assertIsInstance(self.valid_form.cleaned_data['days_till_exp'], int)
















































