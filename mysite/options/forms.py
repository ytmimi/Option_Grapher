import datetime as dt
from django import forms
from django.forms import ValidationError
from options.models import Option_Model, DATE_INPUTS

RF_URL = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

class Search_Form(forms.Form):
	search = forms.CharField(label='',
		widget=forms.TextInput(attrs={'placeholder':'Enter Stock Ticker', 'type':'search'}))


class Option_Form(forms.ModelForm):
	#Current 1 Year Treasury Rate: 2.35% At market close Wed Jun 13, 2018
	interest_rate = forms.FloatField(initial=.0235, min_value=0, max_value=1,
		help_text= f'Reference for <a href="{RF_URL}">Treasury Rates</a>',
		error_messages={
			'max_value': 'Must be less than or equal to 1.',
			'min_value': 'Must be greater than or equal to 0.',
			},)
	expiration_date = forms.DateField(label='Expiration Date', input_formats = DATE_INPUTS,
		error_messages = {'invalid': 'Use date format: Month/Day/Year or Month-Day-Year'})

	class Meta:
		model = Option_Model
		fields = ('position', 'option_type', 'quantity', 'strike_price',
				'stock_price','traded_price', 'interest_rate', 'expiration_date')

	def clean_expiration_date(self):
		expiration = self.cleaned_data['expiration_date']
		if (expiration - dt.date.today()).days >=0:
			return expiration
		raise ValidationError('Sorry, expired options can\'t be analysed.')
