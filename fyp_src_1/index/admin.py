from django.contrib import admin
from .models import Employee, Role, Attendance, WorkSchedule

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('Employee_ID', 'Job_Title','Full_Name','Job_Title','Phone_Number', 'Email_Address', 'Role', 'Start_Date')

class RoleAdmin(admin.ModelAdmin):
	list_display = ('Role_ID', 'Role_Name')

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('Attendance_id', 'Employee_ID', 'DateNow', 'InTime', 'OutTime', 'status')

class WorkScheduleAdmin(admin.ModelAdmin):
	list_display = ('WorkSchedule_id', 'Employee', 'Mark', 'StartDate', 'EndDate', 'StartTime','EndTime')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)

admin.site.register(Attendance, AttendanceAdmin)

admin.site.register(WorkSchedule, WorkScheduleAdmin)