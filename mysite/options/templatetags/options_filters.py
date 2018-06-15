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


@register.inclusion_tag('templatetags/add_table.html')
def table_from_dict(some_dict):
	key = list(some_dict.keys())[0]
	num_of_rows = len(some_dict[key])

	row = []
	for i in range(num_of_rows):
		col = []
		for key in some_dict.keys():
			col.append(some_dict[key][i])
		row.append(col)

	return {
		'header': [x for x in some_dict.keys()],
		'rows': row,
	}

