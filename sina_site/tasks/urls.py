from django.urls import path
from sina_site.tasks import views

urlpatterns = [
    path('', views.TasksIndexView.as_view(), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:id>/', views.TaskShowView.as_view(), name='task_show'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]
