from django.urls import path
from . import views


urlpatterns = [
    #path('', views.index, name='home'),
    path('', views.index, name='home'),
    path('like/', views.handle_like, name='like'),  # Обработка лайков
    path('new_cit', views.newc, name='newc'),
    path('top_cit', views.topc, name='topc')
]
