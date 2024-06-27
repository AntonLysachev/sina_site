from django.urls import path
from sina_site.staff import views

urlpatterns = [
    path('', views.StaffIndexView.as_view(), name='staff'),
    path('<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    path('create/', views.StaffCreateView.as_view(), name='staff_create')
]
