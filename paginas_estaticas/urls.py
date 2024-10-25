from django.urls import path
from paginas_estaticas import views


urlpatterns = [
    path('', views.index, name='index'),
]

