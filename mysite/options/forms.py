from django import forms
import datetime as dt

class Option_Form(forms.Form):
	position = forms.ChoiceField(choices=(('Long', 'Long'), ('Short', 'Short')))
	option_type = forms.ChoiceField(choices=(('Call', 'Call'), ('Put', 'Put')))
	strike_price = forms.DecimalField(decimal_places=2,)
	stock_price = forms.DecimalField(decimal_places=2, )
	traded_price = forms.DecimalField(decimal_places=2,)
	interest_rate = forms.DecimalField(decimal_places=4,)
	exp_date = forms. DateField(label='Expiration Date',
		input_formats=[
			'%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
			'%-m/%d/%Y', '%-m/%d/%y', '%-m-%d-%Y', '%-m-%d-%y',
			'%m/%-d/%Y', '%m/%-d/%y', '%m-%-d-%Y', '%m-%-d-%y',
			'%-m/%-d/%Y', '%-m/%-d/%y', '%-m-%-d-%Y', '%-m-%-d-%y'
		],
		error_messages={'invalid': 'Use date format: Month/Day/Year or Month-Day-Year'})

	def clean_position(self):
		if str(self.cleaned_data['position']) == 'Long':
			return 1
		else:
			return -1

	def clean_option_type(self):
		return str(self.cleaned_data['option_type'])

	def clean_strike_price(self):
		data = float(self.cleaned_data['strike_price'])
		if data >= 0:
			return data
		else:
			raise forms.ValidationError('Strike price must be positive')

	def clean_stock_price(self):
		data = float(self.cleaned_data['stock_price'])
		if data >= 0:
			return data
		else:
			raise forms.ValidationError('Stock price must be positive')

	def clean_traded_price(self):
		data = float(self.cleaned_data['traded_price'])
		if data >= 0:
			return data
		else:
			raise forms.ValidationError('Option price must be positive')

	def clean_interest_rate(self):
		data = float(self.cleaned_data['interest_rate'])
		if data >= 0:
			return data
		else:
			raise forms.ValidationError('Interest rate must be positive')

	def clean_exp_date(self):
		expiration = self.cleaned_data['exp_date']
		now = dt.date.today()
		diff = (expiration - now).days
		if diff >=0:
			return diff
		else:
			raise forms.ValidationError('Sorry, expired options can\'t be analysed.')



