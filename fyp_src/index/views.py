from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Employee

# Create your views here.
def index_home(request):
	return render(request, 'index/index.html')


def index_login(request):

	#if request.POST:
	if request.method == 'POST':


		EmployeeID = request.POST.get('EmployeeID')

		password = request.POST.get('password')
		

		# user authentication, might move this function to another place if needed
		if Employee.objects.filter(Employee_ID=EmployeeID).count() == 1:
			if Employee.objects.filter(Employee_ID=EmployeeID).first().Password == password:
				userObject = Employee.objects.get(Employee_ID=EmployeeID)
				request.session['Employee_ID'] = EmployeeID

				# if user == Sys_Admin
				if userObject.Role.Role_ID == 1:
					return redirect('sys_admin_home')
				elif userObject.Role.Role_ID == 2:
					return redirect('HR_home')
				else:
					return HttpResponse('<h1>youre employee</h1>')

			else:
				messages.error(request, 'Invalid Username or Password')
				return redirect('login')


		else:
			messages.error(request, 'Invalid Username or Password')
			return redirect('login')
	else:
		return render(request, 'index/login.html')



