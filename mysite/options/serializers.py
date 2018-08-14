import json
from options.models import Option_Model
from options import payoff_functions as pf

def option_chart_data():
	option_list = []
	x_values = [0,]
	for option in Option_Model.objects.all():
		option_list.append(
			{'type':option.option_type,
			'pos':option.position,
			'strike':option.strike_price,
			'price':option.traded_price,
			'quantity':option.quantity, })
		x_values.append(option.strike_price)
		x_values.append(option.strike_price*2)

	x_list = sorted(set(x_values))
	payoff = {}
	for x in x_list:
		payoff[x] = 0

	for option in option_list:
		for x in x_list:
			payoff[x] = payoff[x] + pf.option_payoff(option['type'], option['pos'],
							option['strike'], option['price'], option['quantity'], x)

	data = [{'x':x, 'y':y} for x, y in payoff.items()]
	return json.dumps(data)
