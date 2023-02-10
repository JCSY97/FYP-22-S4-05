from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib import messages
from django.urls import reverse
from ..models import Employee,Role,WorkSchedule
from . import form
from django.core.mail import EmailMessage
from django.views.decorators import gzip
import cv2
import threading
from .form import PasswordForm

# Create your views here.
def index_home(request):
	return render(request, 'index/index.html')

def Check_In(request):
	return render(request, 'index/camera.html')

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
					return redirect('Home')

			else:
				messages.error(request, 'Invalid Username or Password')
				return redirect('login')


		else:
			messages.error(request, 'Invalid Username or Password')
			return redirect('login')
	else:
		return render(request, 'index/login.html')


def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')



