from django.urls import path
from read.views import *

app_name = 'read'
urlpatterns = [
    path('<title>/', read_page, name='read_page')
]