from django.contrib import admin
from .models import Employee, Role, WorkSchedule

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('Employee_ID', 'Job_Title','Full_Name','Job_Title','Phone_Number', 'Email_Address', 'Role', 'Start_Date')

class RoleAdmin(admin.ModelAdmin):
	list_display = ('Role_ID', 'Role_Name')

class WorkScheduleAdmin(admin.ModelAdmin):
	list_display = ('WorkSchedule_id', 'Employee', 'Mark', 'StartDate', 'EndDate', 'StartTime','EndTime','AttendanDate','InTime','OutTime')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)


admin.site.register(WorkSchedule, WorkScheduleAdmin)