from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_home(request):
	return render(request, 'index/index.html')


def index_login(request):
	if 'EmployeeID' is not request.session:
		#if request.POST:
		if request.method == 'POST':
			EmployeeID = request.POST.get('EmployeeID')
			password = request.POST.get('password')


	return render(request, 'index/login.html')



