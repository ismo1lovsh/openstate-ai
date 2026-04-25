from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path('', views.network_view, name='view'),
    path('<int:official_id>/', views.network_view, name='view_official'),
    path('<int:official_id>/data/', views.network_data, name='data'),
]
