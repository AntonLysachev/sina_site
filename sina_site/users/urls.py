from django.urls import path
from sina_site.users import views

urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='users'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('create/', views.UserCreateView.as_view(), name='user_create')
]
