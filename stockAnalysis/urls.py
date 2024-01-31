"""
URL configuration for stockAnalysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from app import urls as app_urls 
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include(app_urls)),
    path('', HomeView.as_view(), name="home_view"),
    path('company', CompanyView.as_view(), name="company_view"),
    path('stock/search/', StockSearch.as_view(), name='stock_search'),
    path('stock/suggestions/', StockSuggestions.as_view(), name='stock_suggestions'),
]
