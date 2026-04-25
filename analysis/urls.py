from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.analyzer, name='analyzer'),
    path('wealth-growth/', views.wealth_growth, name='wealth_growth'),
    path('tender-anomaly/', views.tender_anomaly, name='tender_anomaly'),
]
