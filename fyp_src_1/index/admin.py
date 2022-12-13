from django.contrib import admin
from .models import Employee, Role

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('Employee_ID', 'Full_Name', 'Phone_Number', 'Email_Address', 'Role', 'Start_Date')

class RoleAdmin(admin.ModelAdmin):
	list_display = ('Role_ID', 'Role_Name')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)

