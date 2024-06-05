from django.urls import path
from sina_site.customers import views

urlpatterns = [
    path('', views.CustomersIndexView.as_view(), name='customers'),
]
