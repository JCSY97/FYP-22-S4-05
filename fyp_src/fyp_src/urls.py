"""fyp_src URL Configuration

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
from index import views as index_view
from sys_admin import views as sys_admin_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view.index_home, name='index'),
    path('login/', index_view.index_login, name='login'),
    path('logout/', sys_admin_view.logout, name='sys_admin_logout'),
    path('sys_admin/home/', sys_admin_view.sys_admin_home, name='sys_admin_home'), 
    path('sys_admin/view_employees/', sys_admin_view.sys_admin_view_employees, name='sys_admin_view_employees'),

]
