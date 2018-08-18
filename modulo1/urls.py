from django.urls import path

from . import views

app_name = 'modulo1'
urlpatterns = [
    path(r'/', views.IndexView.as_view(), name='index'),
    path(r'/falsaposicao', views.FalsaPosicaoView.as_view(), name='falsaposicao'),
    path(r'/secante', views.SecanteView.as_view(), name='secante'),
    path(r'/muller', views.MullerView.as_view(), name='muller'),
    path(r'/calculafp', views.calculafp, name='calculafp'),
]
