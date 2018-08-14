def option_payoff(option_type, position, strike_price,
					premium, quantity, stock_price):
	''' for a given stock price, the payoff for a call or put is calculated
		position - either 1 or -1 denoting long or short respectively
	'''
	if option_type == 'Call':
		return call_payoff(strike_price, premium, position, quantity, stock_price)
	elif option_type == 'Put':
		return put_payoff(strike_price, premium, position, quantity, stock_price)
	else:
		raise ValueError('option_type must be either Call or Put')

def call_payoff(strike_price: float, premium: float, position: int,
								quantity: int, stock_price: float):
	'''
	quantity - should be >= 1
	position - either 1 or -1 denoting long or short respectively
	return call payoff
	'''
	return (max(stock_price-strike_price, 0)-premium) * position * quantity

def put_payoff(strike_price: float, premium: float, position: int,
								quantity: int, stock_price: float):
	'''
	quantity - should be >= 1
	position - either 1 or -1 denoting long or short respectively
	return put payoff
	'''
	return (max(strike_price - stock_price, 0) - premium) * position * quantity
