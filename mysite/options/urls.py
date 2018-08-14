from django.urls import path
from options import views

app_name = 'options'

urlpatterns = [
	path('', views.option_input, name='form'),
	path('delete/<int:pk>/', views.delete_option, name='delete_option'),
	path('search/', views.stock_option_search, name='search'),
]
