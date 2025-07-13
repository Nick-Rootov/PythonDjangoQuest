from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('new_cit', views.newc, name='newc'),
    path('top_cit', views.topc, name='topc')
]
