from django.urls import path
from . import views

app_name = 'officials'

urlpatterns = [
    path('', views.official_list, name='list'),
    path('<int:pk>/', views.official_detail, name='detail'),
    path('<int:pk>/recalculate/', views.recalculate_risk, name='recalculate'),
]
