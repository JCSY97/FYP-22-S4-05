from django.shortcuts import render, redirect
from index.models import Employee, Role
from django.template import loader
from django.http import HttpResponse

# Create your views here.

# test
def HR_home(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,

		}

		return render(request, 'HR/HR_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def HRProfile(request):
	ViewInfo = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

	Myinfo = Employee.objects.filter(Employee_ID=request.session['Employee_ID'])
	context = {
		'Employee_ID': ViewInfo.Employee_ID,
		'Full_Name': ViewInfo.Full_Name,
		'Role': ViewInfo.Role.Role_Name,
		'EmployeesInfo': Myinfo,
	}

	return render(request, 'HR/HR_profile.html', context)


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
	return redirect('HR_profile')


def HR_Employee(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		data = Employee.objects.all()
		context = {
		    'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
           	'data': data,
		}
		return render(request, 'HR/employees.html',context)


def EmpProfile(request):
	# EmpId = Employee.objects.get(Employee_ID = request.session['Employee_ID'])
	# EmployeeId = Employee.objects.filter(Employee_ID = empid).first()

	# Emp = Employee.objects.get(Employee_ID = Editempid)
	a = int(request.POST.get('EmpID'))
	
	return render(request,'HR/employees-profile.html')

	
	

