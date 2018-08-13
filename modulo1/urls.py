from django.urls import path

from . import views

app_name = 'modulo1'
urlpatterns = [
    path(r'/', views.IndexView.as_view(), name='index'),
    path(r'/falsaposicao', views.FalsaPosicaoView.as_view(), name='falsaposicao'),
    path(r'/calculafp', views.calculafp, name='calculafp'),
]
