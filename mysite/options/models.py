from django.db import models
from wallstreet.blackandscholes import BlackandScholes as BS
from django.core.validators import MinValueValidator
from options import payoff_functions as pf

GREATER_THAN_0 = MinValueValidator(0, 'Must be greater than or equal to 0.')
GREATER_THAN_1 = MinValueValidator(1, 'Must be greater than or equal to 1')
OPTION_TYPES = (('Call', 'Call'), ('Put', 'Put'))

class Option_Model(models.Model):
	stock_ticker = models.CharField(max_length=20, default='Generic Option')
	quantity = models.IntegerField(default=1, validators=[GREATER_THAN_1],)
	position = models.IntegerField()
	option_type = models.CharField(max_length=10, choices=OPTION_TYPES, default='Call',)
	strike_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	stock_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	traded_price = models.FloatField(validators=[GREATER_THAN_0, ],)
	interest_rate = models.FloatField(validators=[GREATER_THAN_0, ],)
	days_till_exp = models.FloatField()
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
			).filter(days_till_exp=option.days_till_exp)

	def save(self, *args, **kwargs):
		option = BS(self.stock_price, self.strike_price, self.days_till_exp,
				self.traded_price, self.interest_rate, str(self.option_type))
		self.iv = round(option.impvol, 5)
		self.delta = round(option.delta(), 5) * self.position * self.quantity
		self.gamma = round(option.gamma(), 5) * self.position * self.quantity
		self.vega = round(option.vega(), 5) * self.position * self.quantity
		self.theta = round(option.theta(), 5) * self.position * self.quantity
		self.rho = round(option.rho(), 5) * self.position * self.quantity
		super().save(*args, **kwargs)

	def option_payoff(self, stock_price):
		'''returns the option payoff given a hypothetical stock price'''
		return pf.option_payoff(self.option_type, self.position, self.strike_price,
								self.traded_price, self.quantity, stock_price)
