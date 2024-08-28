from django.urls import path
from .views import *

urlpatterns = [
    path('home/', indexView.as_view(), name='index'),
]
