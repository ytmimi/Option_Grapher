from django import forms
import datetime as dt
from django.core.validators import MinValueValidator

from options import models


class Search_Form(forms.Form):
	search = forms.CharField(label='', 
		widget=forms.TextInput(attrs={'placeholder':'Enter Stock Ticker', 'type':'search'}))


class Option_Form(forms.ModelForm):
	position = forms.ChoiceField(choices=(('Long', 'Long'), ('Short', 'Short')))
	#http://www.multpl.com/1-year-treasury-rate/ 
	#Current 1 Year Treasury Rate: 2.35% At market close Wed Jun 13, 2018
	interest_rate = forms.FloatField(initial=.0235, min_value=0, max_value=1,
		help_text="1 Year Treasury Rate at market close on 6/13/18",
		error_messages={
			'max_value': 'Must be less than or equal to 1.',
			'min_value': 'Must be greater than or equal to 0.',
		},)
	days_till_exp = forms.DateField(label='Expiration Date',
		input_formats=[
			'%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
			'%-m/%d/%Y', '%-m/%d/%y', '%-m-%d-%Y', '%-m-%d-%y',
			'%m/%-d/%Y', '%m/%-d/%y', '%m-%-d-%Y', '%m-%-d-%y',
			'%-m/%-d/%Y', '%-m/%-d/%y', '%-m-%-d-%Y', '%-m-%-d-%y'],
		error_messages={'invalid': 'Use date format: Month/Day/Year or Month-Day-Year'})

	class Meta:
		model = models.Option_Model
		fields = ('position', 'option_type', 'quantity', 'strike_price', 'stock_price',
			'traded_price', 'interest_rate', 'days_till_exp')

	def clean_position(self):
		if str(self.cleaned_data['position']) == 'Long':
			return 1
		else:
			return -1

	def clean_days_till_exp(self):
		expiration = self.cleaned_data['days_till_exp']
		now = dt.date.today()
		diff = (expiration - now).days
		if diff >=0:
			return diff
		else:
			raise forms.ValidationError('Sorry, expired options can\'t be analysed.')




