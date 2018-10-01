from django.urls import path

from . import views

app_name = 'modulo2'
urlpatterns = [
    path(r'/', views.IndexView.as_view(), name='index'),
    path(r'/GaussJordan', views.GaussJordanView.as_view(), name='GaussJordan'),
    path(r'/gaussJordan', views.GaussJordanView.as_view(), name='gaussJordan'),
    path(r'/newton', views.NewtonView.as_view(), name='newton'),
    path(r'/splines', views.SplinesView.as_view(), name='splines'),
    path(r'/calculaGaussJordan', views.calculaGaussJordan, name='calculaGaussJordan'),
    path(r'/processingSpline', views.processingSpline, name='processingSpline'),
]
