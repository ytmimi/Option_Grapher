import unittest
import os
import sys
#adds the app directory to the path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

import payoff_functions as pf


class Test_Payoff_Functions(unittest.TestCase):
	@classmethod 
	def setUpClass(cls):
		cls.strike_price = 50 
		cls.premeium = 1.24
		cls.quantity = 1
		cls.x = 50


	def test_long_call_payoff_OTM(self):
		# long call _/
		position=1
		for x in range(45, 0, -5):
			payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == -self.premeium)

	def test_long_call_payoff_ATM(self):
		# long call _/
		position=1
		payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, self.x)
		self.assertTrue(payoff == -self.premeium)

	def test_long_call_payoff_ITM(self):
		position=1
		for x in range(55, 2*self.strike_price, 5):
			payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == x-self.strike_price-self.premeium)

	def test_short_call_payoff_OTM(self):
		# short call -\
		position=-1
		for x in range(55, 2*self.strike_price, 5):
			payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == -(x-self.strike_price-self.premeium))

	def test_short_call_payoff_ATM(self):
		# short call -\
		position=-1
		payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, self.x)
		self.assertTrue(payoff == self.premeium)

	def test_short_call_payoff_ITM(self):
		# short call -\
		position=-1
		for x in range(45, 0, -5):
			payoff = pf.call_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == self.premeium)

	def test_long_put_payoff_OTM(self):
		#long put \__
		position=1
		for x in range(55, 2*self.strike_price, 5):
			payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == -self.premeium)
		
	def test_long_put_payoff_ATM(self):
		#long put \__
		position=1
		payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, self.x)
		self.assertTrue(payoff == -self.premeium)

	def test_long_put_payoff_ITM(self):
		#long put \__
		position=1
		for x in range(45, 0, -5):
			payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == (self.strike_price-x-self.premeium))
		
	def test_short_put_payoff_OTM(self):
		#short put /--
		position=-1
		for x in range(45, 0, -5):
			payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == -(self.strike_price-x-self.premeium))

	def test_short_put_payoff_ATM(self):
		#short put /--
		position=-1
		payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, self.x)
		self.assertTrue(payoff == -(self.strike_price-self.x-self.premeium))

	def test_short_put_payoff_ITM(self):
		#short put /--
		position=-1
		for x in range(55, 2*self.strike_price, 5):
			payoff = pf.put_payoff(self.strike_price, self.premeium, position, self.quantity, x)
			self.assertTrue(payoff == self.premeium)


if __name__ =='__main__':
	unittest.main()












