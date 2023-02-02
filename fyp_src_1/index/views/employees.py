from django.shortcuts import render, redirect
from index.models import Employee, Role
from django.contrib import messages
# Create your views here.


def Employee_home(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
		    'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
			'Job_Title' : currentEmployee.Job_Title,
			'Role' : currentEmployee.Role.Role_ID,
			'PFP' : currentEmployee.Profile_Image.url,
           
		}

		return render(request, 'employee/employee_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def Employee_schedule(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
		    'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
		}

		return render(request, 'employee/schedule.html')


def viewProfile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if Role.objects.filter(Role_Name=request.POST.get('role_edit')) == 0:
					messages.error(request, 'No such role')
					return redirect('Profile')


				currentEmployee.Full_Name = request.POST.get('fullName_edit')

				currentEmployee.Phone_Number = request.POST.get('phone')
				currentEmployee.Email_Address = request.POST.get('email')


				currentEmployee.save()

				return redirect('Profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':

				# make sure current password matches
				if request.POST.get('password') == currentEmployee.Password:
					currentEmployee.Password = request.POST.get('newpassword')
					currentEmployee.save()

					messages.info(request, 'Your password has been changed')
					return redirect('Profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('Profile')


		else:
			context = {
				'Employee_ID' : currentEmployee.Employee_ID,
				'Full_Name' : currentEmployee.Full_Name,
				'Role' : currentEmployee.Role.Role_Name,
				'Email' : currentEmployee.Email_Address,
				'Phone' : currentEmployee.Phone_Number,
				'Job_Title' : currentEmployee.Job_Title,
				'PFP' : currentEmployee.Profile_Image.url,
			}
			return render(request, 'employee/users_profile.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')



def UpdateProfile(request, Editempid):
	# EmpId = Employee.objects.get(Employee_ID = request.session['Employee_ID'])
	# EmployeeId = Employee.objects.filter(Employee_ID = empid).first()

	if (request.method == 'POST'):
		UpdateProfile = Employee.objects.get(Employee_ID=Editempid)
		FullName = request.POST.get('fullName')
		Phone = request.POST.get('phone')
		Email = request.POST.get('email')
		UpdateProfile.Full_Name = FullName
		UpdateProfile.Phone_Number = Phone
		UpdateProfile.Email_Address = Email
		UpdateProfile.save()
	return redirect('Home')

