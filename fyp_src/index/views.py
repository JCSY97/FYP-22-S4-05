from django.shortcuts import render
from django.http import HttpResponse

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
				return render(request, 'admin/admin-home.html')

		else:
			messages.error(request, 'Invalid Username or Password')
			return render(request, 'index/login.html')
	else:
		return render(request, 'index/login.html')



