from django import template
from django.urls import reverse
from django.http import HttpResponseRedirect

register = template.Library()

@register.filter(name='dict_key', is_safe = True)
def return_dict_key(d, key):
	'''
	where d is a dictionary and key is a key from
	that dictionary
	'''
	return d[key]

@register.filter(name='multiply', is_safe = True)
def multiply(a, b):
	return a*b



