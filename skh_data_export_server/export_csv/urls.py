from django.urls import path
from export_csv import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('export', views.export_csv, name='export_csv'),
]