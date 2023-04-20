from django.urls import path
from app.views import main_endpoint, main_endpoint_json, usage_endpoint

app_name = 'app'

urlpatterns = [
    path('', main_endpoint, name='main_endpoint'),
    path('json/', main_endpoint_json, name='main_endpoint_json'),
    path('usage/', usage_endpoint, name='usage_endpoint')
]
