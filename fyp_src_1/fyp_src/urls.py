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
from index.views import index,HR,sys_admin,employees


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index_home, name='index'),
    path('login/', index.index_login, name='login'),
    path('logout/', index.logout,name='logout'),
#    path('logout/', sys_admin.logout, name='sys_admin_logout'),
    path('sys_admin/home/', sys_admin.sys_admin_home, name='sys_admin_home'), 
    path('sys_admin/view_employees/', sys_admin.sys_admin_view_employees, name='sys_admin_view_employees'),
    path('sys_admin/view_employees/delete/<int:delete_employee_id>/', sys_admin.delete_employee, name='sys_admin_delete_employee'),
    path('sys_admin/create_user/', sys_admin.sys_admin_create_user, name='sys_admin_create_user'),
    path('sys_admin/user_profile', sys_admin.user_profile, name='sys_admin_user_profile'),
    path('HR/home/', HR.HR_home, name='HR_home'),
#   path('logout/', HR.logout, name='HR_logout'),
    path('employee/employee_home',employees.Employee_home, name='Home'),
    path('users_profile/',index.viewProfile, name='Profile'),
    path('users_profile/edit/<int:Editempid>/',index.UpdateProfile, name='EditProfile'),
    path('employee/schedule', employees.Employee_schedule, name='Employee_schedule'),
]
