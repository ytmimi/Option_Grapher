from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('options/', views.options, name='create'),
    path('options/<slug:ticker>/', views.stock_option_list, name='option_list'),
    path('options/<slug:ticker>/<int:pk>/', views.option_detail, name='option_detail'),
]
