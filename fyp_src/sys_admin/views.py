from django.shortcuts import render, redirect
from index.models import Employee
from django.contrib import messages

# Create your views here.
def sys_admin_home(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
		}

		return render(request, 'sys_admin/sys_admin_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def sys_admin_view_employees(request):

	currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

	allEmployees = Employee.objects.filter(Role=3)
	context={
		'Employee_ID' : currentEmployee.Employee_ID,
		'Full_Name' : currentEmployee.Full_Name,
		'Role' : currentEmployee.Role.Role_Name,
		'Employees' : allEmployees,

	}


	return render(request, 'sys_admin/sys_admin_view_employees.html', context)


def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')
