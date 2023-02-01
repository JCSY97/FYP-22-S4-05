from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib import messages
from django.urls import reverse
from ..models import Employee
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


def viewProfile(request):
		ViewInfo = Employee.objects.get(Employee_ID = request.session['Employee_ID'])

		Myinfo = Employee.objects.filter(Employee_ID = request.session['Employee_ID'])
		context = {
			'Employee_ID' : ViewInfo.Employee_ID,
			'Full_Name' : ViewInfo.Full_Name,
			'Role' : ViewInfo.Role.Role_Name,
			'EmployeesInfo' : Myinfo,
		}

		return render(request, 'index/users_profile.html',context)


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


# def ChangePassword(request, Editempid):
#
# 		UserID = Employee.objects.get(Employee_ID=Editempid)
# 		if request.user.is_authenticated:
# 			form = PasswordForm(request.POST or None)
#
# 			old_password = request.POST.get("old_password")
# 			new_password = request.POST.get("new_password")
# 			re_new_password = request.POST.get("PasswordForm")
# 			if request.POST.get("old_password"):
#
# 				user = Employee.objects.get(Employee_ID=Editempid)
#
# 				# User entered old password is checked against the password in the database below.
# 				if user.check_password('{}'.format(old_password)) == False:
# 					form.set_old_password_flag()
#
# 			if form.is_valid():
#
# 				user.set_password('{}'.format(new_password))
# 				user.save()
# 				update_session_auth_hash(request, user)
#
# 				return redirect('ChangePassword')
#
# 			else:
# 				return render(request, 'users_profile.html', {"form": form})
#
# 		else:
# 			return redirect('login')

def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')



