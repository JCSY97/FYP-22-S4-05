from django.shortcuts import render, redirect
from index.models import Employee

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
		return redirect('login')


def logout(request):
	request.session.flush()
	return render(request, 'index/login.html')
