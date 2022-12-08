from django.contrib import admin
from .models import Employee

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('Employee_ID', 'Full_Name', 'Phone_Number', 'Email_Address', 'Roles')

admin.site.register(Employee, EmployeeAdmin)
