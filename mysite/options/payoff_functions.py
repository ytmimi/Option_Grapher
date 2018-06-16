def option_payoff(option_type, position, strike_price, premium, quantity, x):
	''' for a given stock price x, the payoff for a call or put is calculated
		Note: position should be 1 or -1 denoting Long or Short
	'''
	if option_type == 'Call':
		payoff = call_payoff(strike_price, premium, position, quantity, x)
	else:
		payoff = put_payoff(strike_price, premium, position, quantity, x)
	return payoff

def call_payoff(strike_price, premium, position, quantity, x):
	''' 
	strike_price- float representing the excersie price of the option
	premium- float representing the price paid for the option
	position- either 1 or -1 denoting long or short respectively
	x- a float or int representing a given stock price
	'''
	return (max(x-strike_price, 0)-premium) * position * quantity

def put_payoff(strike_price, premium, position, quantity, x):
	'''
	strike_price- float representing the excersie price of the option
	premium- float representing the price paid for the option
	position- either 1 or -1 denoting long or short respectively
	x- a float or int representing a given stock price
	'''
	return (max(strike_price - x, 0) - premium) * position * quantity


				
			
			

