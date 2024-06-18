from django.urls import path
from sina_site.shift_schedule import views

urlpatterns = [
    path('', views.Shift_scheduleIndexView.as_view(), name='shift_schedule'),
]