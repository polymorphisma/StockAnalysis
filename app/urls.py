from django.contrib import admin
from django.urls import path, include


from .views import (
    StockView,
    HomeView
)

urlpatterns = [
    path('v1/stock_data', StockView.as_view()),
]

