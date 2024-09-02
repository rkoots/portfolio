from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_list, name='portfolio-list'),
    path('chart', views.portfolio_chart, name='portfolio-chart'),
]
