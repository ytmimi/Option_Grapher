from django.db import models
from wallstreet.blackandscholes import BlackandScholes as BS
from django.core.validators import MinValueValidator


def same_option(option):
	return Option_Model.objects.filter(position=option.position
		).filter(option_type=option.option_type
		).filter(strike_price=option.strike_price
		).filter(stock_price=option.stock_price
		).filter(traded_price=option.traded_price
		).filter(interest_rate=option.interest_rate
		).filter(days_till_exp=option.days_till_exp)

# Create your models here.
class Option_Model(models.Model):
	stock_ticker = models.CharField(max_length=20, default='Generic Option')
	quantity = models.IntegerField(default=1,
		validators=[MinValueValidator(1, 'Must be greater than or equal to 1')],)
	position = models.IntegerField()
	option_type = models.CharField(max_length=10, default='Call',
					choices=(('Call', 'Call'), ('Put', 'Put')),)
	strike_price = models.FloatField(
		validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')],)
	stock_price = models.FloatField(
		validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')],)
	traded_price = models.FloatField(
		validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')],)
	interest_rate = models.FloatField(
		validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')],)
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
		self.delta = round(option.delta(), 5)*self.position*self.quantity
		self.gamma = round(option.gamma(), 5)*self.position*self.quantity
		self.vega = round(option.vega(), 5)*self.position*self.quantity
		self.theta = round(option.theta(), 5)*self.position*self.quantity
		self.rho = round(option.rho(), 5)*self.position*self.quantity
		super().save(*args, **kwargs)
