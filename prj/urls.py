from django.urls import path
from app.views import main_endpoint
from app.views import usage_endpoint

app_name = 'app'

urlpatterns = [
    path('', main_endpoint, name='main_endpoint'),
    path('usage/', usage_endpoint, name='usage_endpoint')
]
