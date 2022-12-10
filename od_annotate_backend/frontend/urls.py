from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "frontend"

urlpatterns = [
    path('semtab', views.semtab, name="semtab"),


]
