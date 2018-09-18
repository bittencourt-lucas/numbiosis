from django.urls import path

from . import views

app_name = 'modulo2'
urlpatterns = [
    path(r'/', views.IndexView.as_view(), name='index'),
    path(r'/GaussJordan', views.GaussJordanView.as_view(), name='GaussJordan'),
    path(r'/calculaGaussJordan', views.calculaGaussJordan, name='calculaGaussJordan'),
   
]