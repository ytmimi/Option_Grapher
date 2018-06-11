from django.db import models
from wallstreet.blackandscholes import BlackandScholes as BS

# Create your models here.
class Option_Model(models.Model):
	position = models.IntegerField()
	option_type = models.CharField(max_length=10, choices=(('Call', 'Call'), ('Put', 'Put')))
	strike_price = models.FloatField()
	stock_price = models.FloatField()
	traded_price = models.FloatField()
	interest_rate = models.FloatField()
	days_till_exp = models.FloatField()
	iv = models.FloatField(null=True, blank=True)
	delta = models.FloatField(null=True, blank=True)
	gamma = models.FloatField(null=True, blank=True)
	vega = models.FloatField(null=True, blank=True)
	theta = models.FloatField(null=True, blank=True)
	rho = models.FloatField(null=True, blank=True)

	def __str__(self):
		if self.position == 1:
			position = 'Long'
		else:
			position = 'Short'
		return f'{self.strike_price} {position} {self.option_type}'

	def save(self, *args, **kwargs):
		option = BS(self.stock_price, self.strike_price, self.days_till_exp, 
				self.traded_price, self.interest_rate, str(self.option_type))
		self.iv = round(option.impvol, 5)
		self.delta = round(option.delta(), 5)*self.position
		self.gamma = round(option.gamma(), 5)*self.position
		self.vega = round(option.vega(), 5)*self.position
		self.theta = round(option.theta(), 5)*self.position
		self.rho = round(option.rho(), 5)*self.position
		super().save(*args, **kwargs)


	def is_the_same(self, option_model):
		return (self.position == option_model.position  
			and self.option_type == option_model.option_type
			and self.strike_price == option_model.strike_price
			and self.stock_price == option_model.stock_price
			and self.traded_price == option_model.traded_price
			and self.interest_rate == option_model.interest_rate
			and self.days_till_exp == option_model.days_till_exp)