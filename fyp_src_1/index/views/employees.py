from django.shortcuts import render, redirect
from index.models import Employee, Role

# Create your views here.


def Employee_home(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		context = {
		    'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
           
		}

		return render(request, 'employee/employee_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')



def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')
