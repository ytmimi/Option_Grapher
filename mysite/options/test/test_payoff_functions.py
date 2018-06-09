import unittest
import os
import sys
#adds the app directory to the path
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

import payoff_functions as pf


class Test_Payoff_Functions(unittest.TestCase):

	def test_long_call_payoff_OTM(self):
		# long call _/
		strike_price=50
		premeium=1.24
		position=1
		for x in range(45, 0, -5):
			payoff = pf.call_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == -premeium)

	def test_long_call_payoff_ATM(self):
		# long call _/
		strike_price=50
		premeium=1.24
		position=1
		x=50
		payoff = pf.call_payoff(strike_price, premeium, position, x)
		self.assertTrue(payoff == -premeium)

	def test_long_call_payoff_ITM(self):
		# long call _/
		strike_price=50
		premeium=1.24
		position=1
		for x in range(55, 2*strike_price, 5):
			payoff = pf.call_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == x-strike_price-premeium)

	def test_short_call_payoff_OTM(self):
		# short call -\
		strike_price=50
		premeium=1.24
		position=-1
		for x in range(55, 2*strike_price, 5):
			payoff = pf.call_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == -(x-strike_price-premeium))

	def test_short_call_payoff_ATM(self):
		# short call -\
		strike_price=50
		premeium=1.24
		position=-1
		x = 50
		payoff = pf.call_payoff(strike_price, premeium, position, x)
		self.assertTrue(payoff == premeium)

	def test_short_call_payoff_ITM(self):
		# short call -\
		strike_price=50
		premeium=1.24
		position=-1
		for x in range(45, 0, -5):
			payoff = pf.call_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == premeium)

	def test_long_put_payoff_OTM(self):
		#long put \__
		strike_price=50
		premeium=1.24
		position=1
		for x in range(55, 2*strike_price, 5):
			payoff = pf.put_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == -premeium)
		
	def test_long_put_payoff_ATM(self):
		#long put \__
		strike_price=50
		premeium=1.24
		position=1
		x=50
		payoff = pf.put_payoff(strike_price, premeium, position, x)
		self.assertTrue(payoff == -premeium)

	def test_long_put_payoff_ITM(self):
		#long put \__
		strike_price=50
		premeium=1.24
		position=1
		for x in range(45, 0, -5):
			payoff = pf.put_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == (strike_price-x-premeium))
		
	def test_short_put_payoff_OTM(self):
		#short put /--
		strike_price=50
		premeium=1.24
		position=-1
		for x in range(45, 0, -5):
			payoff = pf.put_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == -(strike_price-x-premeium))

	def test_short_put_payoff_ATM(self):
		#short put /--
		strike_price=50
		premeium=1.24
		position=-1
		x=50
		payoff = pf.put_payoff(strike_price, premeium, position, x)
		self.assertTrue(payoff == -(strike_price-x-premeium))

	def test_short_put_payoff_ITM(self):
		#short put /--
		strike_price=50
		premeium=1.24
		position=-1
		for x in range(55, 2*strike_price, 5):
			payoff = pf.put_payoff(strike_price, premeium, position, x)
			self.assertTrue(payoff == premeium)


if __name__ =='__main__':
	unittest.main()












