from django import template
register = template.Library()

@register.filter(name='dict_key', is_safe = True)
def return_dict_key(d, key):
	'''
	where d is a dictionary and key is a key from
	that dictionary
	'''
	return d[key]