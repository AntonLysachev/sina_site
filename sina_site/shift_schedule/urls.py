from django.urls import path
from sina_site.shift_schedule import views

urlpatterns = [
    path('', views.ShiftScheduleIndexView.as_view(), name='shift_schedule'),
    path('try', views.ShiftScheduleTryView.as_view(), name='shift_try'),
    path('create/', views.ShiftScheduleCreateView.as_view(), name='shift_create'),
    path('<str:slug>/update/', views.ShiftScheduleUpdateView.as_view(), name='shift_update'),
]