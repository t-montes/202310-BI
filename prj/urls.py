from django.urls import path
from app.views import main_endpoint, main_endpoint_json, main_endpoint_csvtext, analytics_endpoint

app_name = 'app'

urlpatterns = [
    path('', main_endpoint, name='main_endpoint'),
    path('json/', main_endpoint_json, name='main_endpoint_json'),
    path('csvtext/', main_endpoint_csvtext, name='main_endpoint_csvtext'),
    path('analytics/', analytics_endpoint, name='analytics_endpoint')
]
