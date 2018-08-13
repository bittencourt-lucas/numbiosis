from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path(r'', views.HomeView.as_view(), name='index'),
]
