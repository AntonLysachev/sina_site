from django.urls import path
from sina_site.labels import views


urlpatterns = [
    path('', views.LabelsIndexView.as_view(), name='labels'),
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
    path('create/', views.LabelCreateView.as_view(), name='label_create')
]
