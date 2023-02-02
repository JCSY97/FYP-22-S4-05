from django.shortcuts import render, redirect
from index.models import Employee, Role,Attendance
from django.contrib import messages

from django.http import HttpResponse


def HR_home(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		AttendanceData = Attendance.objects.filter(Employee_ID_id= request.session['Employee_ID'])
		context = {
			'Role' : currentEmployee.Role.Role_ID,
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
			'Job_Title' : currentEmployee.Job_Title,
			'PFP' : currentEmployee.Profile_Image.url,
			'data':AttendanceData,
		}


		return render(request, 'HR/HR_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def HR_Profile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if Role.objects.filter(Role_Name=request.POST.get('role_edit')) == 0:
					messages.error(request, 'No such role')
					return redirect('HR_Profile')


				currentEmployee.Full_Name = request.POST.get('fullName_edit')

				currentEmployee.Phone_Number = request.POST.get('phone')
				currentEmployee.Email_Address = request.POST.get('email')


				currentEmployee.save()

				return redirect('HR_Profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':

				# make sure current password matches
				if request.POST.get('password') == currentEmployee.Password:
					currentEmployee.Password = request.POST.get('newpassword')
					currentEmployee.save()

					messages.info(request, 'Your password has been changed')
					return redirect('HR_Profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('HR_Profile')


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
			return render(request, 'HR/HR_profile.html', context)
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
	return redirect('HR_Profile')


def HR_EmployeePage(request):
	currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
	data = Employee.objects.all()
	context = {
		'Employee_ID' : currentEmployee.Employee_ID,
		'Job_Title' : currentEmployee.Job_Title,
		'Full_Name' : currentEmployee.Full_Name,
		'data': data,
	}
	return render(request, 'HR/employees.html', context)


def HR_EmpProfile(request):
	if request.method == 'GET':
		EmpId = request.GET.get('id')
		# print(EmpId,"testes")
		
		Myinfo = Employee.objects.get(Employee_ID = EmpId)
		context = {
			'Employee_ID': Myinfo.Employee_ID,
			'Full_Name': Myinfo.Full_Name,
			'Role': Myinfo.Role.Role_Name,
			'Job_Title' : Myinfo.Job_Title,
			'Email' : Myinfo.Email_Address,
			'Phone' : Myinfo.Phone_Number,
			'PFP' : Myinfo.Profile_Image.url,
		}
		return render(request, 'HR/employees-profile.html', context)
	# return HttpResponse(EmpId)


def HR_View_Schedule(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
			'Role' : currentEmployee.Role.Role_ID,
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
			'Job_Title' : currentEmployee.Job_Title,
			'PFP' : currentEmployee.Profile_Image.url,
		}

		return render(request, 'HR/schedule.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def Change_Status(request):
	
	return render(request, 'HR/change-status.html')


def Employee_Schedule(request):

	return render(request, 'HR/employeesview_schedule.html')

def Emp_update_Schedule(request):

	return render(request, 'HR/upload-schedule.html')