from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from wallstreet.blackandscholes import BlackandScholes as BS
from options import forms
from options import models
from options.serializers import option_chart_data
from options.scrape_data import Yahoo_Option_Scraper

# Create your views here.

def delete_option(request, pk):
	option = models.Option_Model.objects.filter(pk=pk)
	option.delete()
	return HttpResponseRedirect(reverse('options:form'))


def option_input(request):
	form = forms.Option_Form()
	if request.method == 'POST':
		form = forms.Option_Form(request.POST)
		if form.is_valid():
			#cleaned position is either 1 or -1 if long or short respectively
			quantity = form.cleaned_data['quantity']
			position = form.cleaned_data['position']
			s = form.cleaned_data['stock_price']
			k = form.cleaned_data['strike_price']
			t = form.cleaned_data['days_till_exp'] / 365
			p = form.cleaned_data['traded_price']
			r = form.cleaned_data['interest_rate']
			type_ = form.cleaned_data['option_type']

			#creates an instance of the option model
			option_model = models.Option_Model(quantity=quantity, position=position,option_type=type_,
				strike_price=k, stock_price=s,traded_price=p,interest_rate=r,days_till_exp=t,)
			#checks if the option submitted by the form isn't already in the database
			if len(models.same_option(option_model)) == 0:
				option_model.save()
	
	data = {'form': form,
			'model':models.Option_Model.objects.all(),
			'payoff': option_chart_data(),}
	return render(request, 'options/options_forms.html', data)



def stock_option_search(request):
	if request.method == 'POST':
		form = forms.Search_Form(request.POST)
		if form.is_valid():
			ticker = form.cleaned_data['search']
			# import pdb; pdb.set_trace()
			try:
				date = request.POST['dates']
				scraper = Yahoo_Option_Scraper(ticker, date)
			except KeyError:
				scraper = Yahoo_Option_Scraper(ticker)
			
			data = {'form': form,
				'ticker':ticker,
				'name': scraper.get_company_name(),
				'stock_price': scraper.get_stock_price(),
				'exp_dates':scraper.exp_dates,
				'calls': scraper.get_option_table(),
				'puts':	scraper.get_option_table(call=False),				
			}
			return render(request, 'options/options_scrape_form.html', data)

	data = {'form':forms.Search_Form()}
	return render(request, 'options/options_scrape_form.html', data)

	



