from django.urls import path
from sina_site.analytics import views

urlpatterns = [
    path('', views.AnalyticsIndexView.as_view(), name='analytics'),
]