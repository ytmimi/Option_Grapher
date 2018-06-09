from django.shortcuts import render
from wallstreet.blackandscholes import BlackandScholes as BS
from options import forms
from options import payoff_functions as pf

# Create your views here.
def option_input(request):
	form = forms.Option_Form()

	if request.method == 'POST':
		form = forms.Option_Form(request.POST)
		if form.is_valid():
			#cleaned position is either 1 or -1 if long or short respectively
			position = form.cleaned_data['position']
			s = form.cleaned_data['stock_price']
			k = form.cleaned_data['strike_price']
			t = form.cleaned_data['exp_date'] / 365
			p = form.cleaned_data['traded_price']
			r = form.cleaned_data['interest_rate']
			type_ = form.cleaned_data['option_type']

			option = BS(s, k, t, p, r, type_)

			data = {'form':form,
					'option':{
						'Implied Volatility': round(option.impvol, 5),
						'Delta':round(option.delta(), 5)*position,
						'Gamma':round(option.gamma(), 5)*position,
						'Vega': round(option.vega(), 5)*position,
						'Theta': round(option.theta(), 5)*position,
						'Rho': round(option.rho(), 5)*position,
					},
					'payoff': pf.payoff_to_json(type_, position, k, p)
			}
			return render(request, 'options/options_forms.html', data)
	data = {'form':form}
	return render(request, 'options/options_forms.html', data)


	



