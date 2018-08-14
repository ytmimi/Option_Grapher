from django.shortcuts import render
from django.urls import reverse
from options.forms import Search_Form, Option_Form
from django.http import HttpResponseRedirect
from options.models import Option_Model
from options.serializers import option_chart_data
from options.scrape_data import Yahoo_Option_Scraper



def delete_option(request, pk):
	option = Option_Model.objects.filter(pk=pk)
	option.delete()
	return HttpResponseRedirect(reverse('options:form'))

def option_input(request):
	form = Option_Form()
	if request.method == 'POST':
		form = Option_Form(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			position = form.cleaned_data['position']
			s = form.cleaned_data['stock_price']
			k = form.cleaned_data['strike_price']
			t = form.cleaned_data['days_till_exp']
			p = form.cleaned_data['traded_price']
			r = form.cleaned_data['interest_rate']
			type_ = form.cleaned_data['option_type']

			option_model = Option_Model(quantity=quantity, position=position,option_type=type_,
				strike_price=k, stock_price=s,traded_price=p,interest_rate=r,days_till_exp=t,)
			if len(Option_Model.already_exists(option_model)) == 0:
				option_model.save()

	data = {'form': form,
			'model': Option_Model.objects.all(),
			'payoff': option_chart_data(),}
	return render(request, 'options/options_forms.html', data)

def stock_option_search(request):
	if request.method == 'POST':
		form = Search_Form(request.POST)
		if form.is_valid():
			ticker = form.cleaned_data['search']
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

	data = {'form':Search_Form()}
	return render(request, 'options/options_scrape_form.html', data)
