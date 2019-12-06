import datetime as dt
from django.db import models
from wallstreet.blackandscholes import BlackandScholes as BS
from django.core.validators import MinValueValidator
from options import payoff_functions as pf

GREATER_THAN_0 = MinValueValidator(0, 'Must be greater than or equal to 0.')
GREATER_THAN_1 = MinValueValidator(1, 'Must be greater than or equal to 1')
OPTION_TYPES = (('Call', 'Call'), ('Put', 'Put'))
POSITIONS = (('Long', 'Long'), ('Short', 'Short'))
DATE_INPUTS = [
	'%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y',
	'%-m/%d/%Y', '%-m/%d/%y', '%-m-%d-%Y', '%-m-%d-%y',
	'%m/%-d/%Y', '%m/%-d/%y', '%m-%-d-%Y', '%m-%-d-%y',
	'%-m/%-d/%Y', '%-m/%-d/%y', '%-m-%-d-%Y', '%-m-%-d-%y',
	'%Y/%m/%d', '%Y-%m-%d'
]

class Option_Model(models.Model):
	stock_ticker = models.CharField(max_length=20, default='GENERIC OPTION')
	quantity = models.IntegerField(default=1, validators=[GREATER_THAN_1],)
	position = models.CharField(max_length=10, choices=POSITIONS, default='Long')
	option_type = models.CharField(max_length=5, choices=OPTION_TYPES, default='Call',)
	strike_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	stock_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	traded_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	interest_rate = models.FloatField(validators=[GREATER_THAN_0, ],)
	expiration_date = models.DateField()
	days_till_exp = models.FloatField(blank=True)
	iv = models.FloatField(null=True, blank=True)
	delta = models.FloatField(null=True, blank=True)
	gamma = models.FloatField(null=True, blank=True)
	vega = models.FloatField(null=True, blank=True)
	theta = models.FloatField(null=True, blank=True)
	rho = models.FloatField(null=True, blank=True)

	def __str__(self):
		if self.position == 1:
			return f'{self.strike_price} Long {self.option_type}'
		return f'{self.strike_price} Short {self.option_type}'

	@classmethod
	def already_exists(cls, option):
		return cls.objects.filter(position=option.position
			).filter(option_type=option.option_type
			).filter(strike_price=option.strike_price
			).filter(stock_price=option.stock_price
			).filter(traded_price=option.traded_price
			).filter(interest_rate=option.interest_rate
			).filter(expiration_date=option.expiration_date)

	def save(self, *args, **kwargs):
		days_per_year = self.days_till_exp/ 365
		position = self.convert_position()
		option = BS(self.stock_price, self.strike_price, days_per_year,
				self.traded_price, self.interest_rate, str(self.option_type))
		self.iv = round(option.impvol, 5)
		self.delta = round(option.delta(), 5) * position * self.quantity
		self.gamma = round(option.gamma(), 5) * position * self.quantity
		self.vega = round(option.vega(), 5) * position * self.quantity
		self.theta = round(option.theta(), 5) * position * self.quantity
		self.rho = round(option.rho(), 5) * position * self.quantity
		super().save(*args, **kwargs)

	def convert_position(self):
		'''returns a numeric representation of position'''
		if self.position == 'Long':
			return 1
		return -1

	#A MUST CALL METHOD. CONSIDER ADDING TO SAVE FUNCTION
	def set_days_till_expiration(self):
		self.days_till_exp = (self.expiration_date - dt.date.today()).days

	def option_payoff(self, stock_price):
		'''returns the option payoff given a hypothetical stock price'''
		position = self.convert_position()
		return pf.option_payoff(self.option_type, position, self.strike_price,
								self.traded_price, self.quantity, stock_price)
	@classmethod
	def all_tickers(cls):
		return set([option['stock_ticker'] for option in cls.objects.values('stock_ticker')])
