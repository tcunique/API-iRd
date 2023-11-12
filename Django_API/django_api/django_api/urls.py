"""django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_ import views

from django_.views import airflow_dags

urlpatterns = [
    path("admin/", admin.site.urls),
    path('list_dag/', airflow_dags, name='list_dag'),
    path('delete/<str:dag_id>/', views.delete_dags, name='delete'),
    path('pause/<str:dag_id>/', views.pause, name='pause'),
    path('trigger/<str:dag_id>/', views.launch, name='trigger'),
    path('generate_dag/', views.create_dag, name='generate_dag'),
    path("check_dag_status/", views.check_dag_status, name="check_dag_status"),
]

