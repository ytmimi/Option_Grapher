import json

#pre defined functions used to calculate option payoffs
def option_payoff(option_type, position, strike_price, premium, x):
	''' for a given stock price x, the payoff for a call or put is calculated
		Note: position should be 1 or -1 denoting Long or Short
	'''
	if option_type == 'Call':
		payoff = call_payoff(strike_price, premium, position, x)
	else:
		payoff = put_payoff(strike_price, premium, position, x)
	return payoff

def call_payoff(strike_price, premium, position, x):
	''' 
	strike_price- float representing the excersie price of the option
	premium- float representing the price paid for the option
	position- either 1 or -1 depending on if long or short respectively
	x- a float or int representing a given stock price
	'''
	if x < strike_price:
		payoff = -premium
	else:
		payoff = x - strike_price - premium

	return payoff*position

def put_payoff(strike_price, premium, position, x):
	'''
	strike_price- float representing the excersie price of the option
	premium- float representing the price paid for the option
	position- either 1 or -1 depending on if long or short respectively
	x- a float or int representing a given stock price
	'''
	if x > strike_price:
		payoff = -premium
	else:
		payoff = strike_price - x - premium
	return payoff*position

def payoff_to_json(option_type, position, strike_price, premium,):
	'''
	see put_payoff and call_payoff for details on the arguments
	formats final result to JSON
	'''
	# x_list = [x for x in range(0,int(strike_price*2), 5)]
	x_list = [0, strike_price, 2*strike_price]
	y_list = []
	for x in x_list:
		y = option_payoff(option_type, position, strike_price, premium, x)
		y_list.append(y)
	#Using jason.dumps leave me with a string containing:
	# "[{&quot;x&quot;: 0, &quot;y&quot;: -4.0},...]". Not sure why
	json_ob = json.dumps({"x": x_list, "y": y_list})
	return json_ob


				
			
			

