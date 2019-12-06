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
def table_from_dict(input: dict):
	table = input['table']
	html_id = input['id']
	key = list(table.keys())[0]
	num_of_rows = len(table[key])

	row = []
	for i in range(num_of_rows):
		col = []
		for key in table.keys():
			col.append(table[key][i])
		row.append(col)

	return {
		'header': [x for x in table.keys()],
		'rows': row,
		'id':html_id
	}

@register.filter(name='set_selector_value', is_safe=True)
def set_selector_value(exp_dates: dict, date):
	for text, timestamp in exp_dates.items():
		if timestamp == date:
			return text
