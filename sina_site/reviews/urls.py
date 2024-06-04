from django.urls import path
from sina_site.reviews import views

urlpatterns = [
    path('', views.ReviewsIndexView.as_view(), name='reviews'),
]