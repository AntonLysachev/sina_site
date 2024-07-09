from django.urls import path
from sina_site.shift_schedule import views

urlpatterns = [
    path('', views.ShiftScheduleIndexView.as_view(), name='shift_schedule'),
    path('<str:slug>/create', views.ShiftScheduleCreateView.as_view(), name='shift_create'),
    path('<str:slug>/update/', views.ShiftScheduleUpdateView.as_view(), name='shift_update'),
    path('chuse_week/', views.ChuseWeekView.as_view(), name='chuse_week')
]