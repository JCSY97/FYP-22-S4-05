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
			'PFP' : currentEmployee.Profile_Image.url,
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
		'PFP' : currentEmployee.Profile_Image.url,
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



		#if employee_ID is taken
		if Employee.objects.filter(Employee_ID=New_Employee_ID).exists():
			messages.error(request, 'There already exist such Employee ID')
			return redirect('sys_admin_create_user')

		elif New_Password != New_Password_2:
			messages.error(request, 'Your passwords does not match')
			return redirect('sys_admin_create_user')
		else:
			New_Role = Role.objects.get(Role_Name=New_Role_Name)

			# if have PFP
			if request.FILES['profilepic']:
				New_PFP = request.FILES['profilepic']
				new_employee = Employee(Employee_ID=New_Employee_ID, Full_Name=New_Employee_Full_Name, Phone_Number=New_Phone_Number,
									 Email_Address=New_Email_Address, Role=New_Role, Password=New_Password, Profile_Image=New_PFP)
			else:
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

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if Role.objects.filter(Role_Name=request.POST.get('role_edit')) == 0:
					messages.error(request, 'No such role')
					return redirect('sys_admin_user_profile')


				currentEmployee.Full_Name = request.POST.get('fullName_edit')
				
				Role_edit = Role.objects.get(Role_Name=request.POST.get('role_edit'))
				currentEmployee.Role = Role_edit

				currentEmployee.Phone_Number = request.POST.get('phone_edit')
				currentEmployee.Email_Address = request.POST.get('email_edit')


				currentEmployee.save()

				return redirect('sys_admin_user_profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':

				# make sure current password matches
				if request.POST.get('password') == currentEmployee.Password:
					currentEmployee.Password = request.POST.get('newpassword')
					currentEmployee.save()

					messages.info(request, 'Your password has been changed')
					return redirect('sys_admin_user_profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('sys_admin_user_profile')


		else:
			context = {
				'Employee_ID' : currentEmployee.Employee_ID,
				'Full_Name' : currentEmployee.Full_Name,
				'Role' : currentEmployee.Role.Role_Name,
				'Email' : currentEmployee.Email_Address,
				'Phone' : currentEmployee.Phone_Number,
				'PFP' : currentEmployee.Profile_Image.url,
			}
			return render(request, 'sys_admin/sys_admin_user_profile.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')



def edit_employee(request, edit_employee_id):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		if request.method == 'POST':
			edit_employee = Employee.objects.get(Employee_ID=edit_employee_id)

			edit_employee.Full_Name = request.POST.get('fullName')
			edit_employee.Role = Role.objects.get(Role_Name=request.POST.get('newRole'))
			edit_employee.Phone_Number = request.POST.get('phone')
			edit_employee.Email_Address = request.POST.get('email')

			edit_emplyee.save()

			return redirect('/sys_admin/view_employees/edit/' + str(edit_employee_id))

		else:
			if Employee.objects.filter(Employee_ID=edit_employee_id).count() == 1:
				edit_employee = Employee.objects.get(Employee_ID=edit_employee_id)
				context = {
					'edit_employee_id' : edit_employee_id,
					'edit_employee_full_name' : edit_employee.Full_Name,
					'edit_employee_role' : edit_employee.Role,
					'edit_employee_phone' : edit_employee.Phone_Number,
					'edit_employee_email' : edit_employee.Email_Address,
					'edit_employee_pfp' : edit_employee.Profile_Image.url,
					'Full_Name' : currentEmployee.Full_Name,
					'Role' : currentEmployee.Role.Role_Name,
					'PFP' : currentEmployee.Profile_Image.url,
				}

			return render(request, 'sys_admin/sys_admin_edit_employee.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')

def schedule(request):

	return render(request, 'sys_admin/sys_admin_schedule.html')

def upload_img(request):
	return render(request, 'sys_admin/sys_admin_upload_img.html')


def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')
