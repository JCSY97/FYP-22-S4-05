from django.shortcuts import render, redirect, reverse
from index.models import Employee, Role
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

	allEmployees = Employee.objects.all()
	context={
		'Employee_ID' : currentEmployee.Employee_ID,
		'Full_Name' : currentEmployee.Full_Name,
		'Role' : currentEmployee.Role.Role_Name,
		'Employees' : allEmployees,
	}

	return render(request, 'sys_admin/sys_admin_view_employees.html', context)



def sys_admin_create_user(request):
	if request.method == 'POST':
		New_Employee_Full_Name = request.POST.get('name')
		New_Employee_ID = request.POST.get('EmployeeID')
		New_Phone_Number = request.POST.get('phone')
		New_Email_Address = request.POST.get('email')
		New_Role_Name = request.POST.get('roles')

		# do password hash later
		New_Password = request.POST.get('password')
		New_Password_2 = request.POST.get('password2')


		# rmb to do profilepic later
		#profilepic

		#if employee_ID is taken
		if Employee.objects.filter(Employee_ID=New_Employee_ID).exists():
			messages.error(request, 'There already exist such Employee ID')
			return redirect('sys_admin_create_user')

		if New_Password != New_Password_2:
			messages.error(request, 'Your passwords does not match')
			return redirect('sys_admin_create_user')
		else:
			New_Role = Role.objects.get(Role_Name=New_Role_Name)

			new_employee = Employee(Employee_ID=New_Employee_ID, Full_Name=New_Employee_Full_Name, Phone_Number=New_Phone_Number,
									 Email_Address=New_Email_Address, Role=New_Role, Password=New_Password)
			new_employee.save()
			messages.success(request, 'New account has been created')
			return redirect('sys_admin_create_user')



	else:
		return render(request, 'sys_admin/sys_admin_create_user.html')


def delete_employee(request, delete_employee_id):
	if Employee.objects.filter(Employee_ID=delete_employee_id).count() == 1:
		Employee_to_delete = Employee.objects.get(Employee_ID=delete_employee_id)
		Employee_to_delete.delete()

	return redirect('sys_admin_view_employees')


def user_profile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		context = {
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
			'Role' : currentEmployee.Role.Role_Name,
			'Email' : currentEmployee.Email_Address,
			'Phone' : currentEmployee.Phone_Number,
		}
		return render(request, 'sys_admin/sys_admin_user_profile.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')


def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')
