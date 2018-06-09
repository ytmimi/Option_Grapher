from django.urls import path
from . import views

app_name = 'options'

urlpatterns = [
	path('', views.option_input, name='form'),

]
