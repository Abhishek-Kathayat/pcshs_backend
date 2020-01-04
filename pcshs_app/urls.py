from django.urls import path
from . import views

urlpatterns = [
    path('tests/heartdisease/dataupload', views.processHeartData),
    path('tests/arrhythmia/dataupload', views.processECGData)
]
