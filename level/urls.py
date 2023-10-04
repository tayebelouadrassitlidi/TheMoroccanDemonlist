from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mainlist/', views.level_mainlist, name='level_mainlist'),
    path('extendedlist/', views.level_extendedlist, name='level_extendedlist'),
    path('legacylist/', views.level_legacylist, name='level_legacylist'),
    path('level/<int:level_id>/', views.level_detail, name='level_detail'),
]