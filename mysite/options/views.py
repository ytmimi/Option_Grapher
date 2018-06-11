from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from wallstreet.blackandscholes import BlackandScholes as BS
from options import forms
from options import models
from options.serializers import option_chart_data

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
			position = form.cleaned_data['position']
			s = form.cleaned_data['stock_price']
			k = form.cleaned_data['strike_price']
			t = form.cleaned_data['exp_date'] / 365
			p = form.cleaned_data['traded_price']
			r = form.cleaned_data['interest_rate']
			type_ = form.cleaned_data['option_type']

			#creates an instance of the option model
			option_model = models.Option_Model(position=position,option_type=type_,strike_price=k,
				stock_price=s,traded_price=p,interest_rate=r,days_till_exp=t,)
			#come back and figure out a better way to do this
			if len(models.Option_Model.objects.all()) > 0:
				for model in models.Option_Model.objects.all():
					if(not option_model.is_the_same(model)):
						#only save the model if it doesn't match a pre existing option
						option_model.save()
						break
			else:
				option_model.save()
			
			data = {'form':form,
					'payoff': option_chart_data(),
					'model':models.Option_Model.objects.all()
			}
			return render(request, 'options/options_forms.html', data)
	data = {'form':form, 
			'model':models.Option_Model.objects.all(),
			'payoff': option_chart_data(),
	}
	return render(request, 'options/options_forms.html', data)


	



