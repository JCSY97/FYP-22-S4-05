from django.shortcuts import render, redirect, reverse
from index.models import Employee, Role,WorkSchedule
from django.contrib import messages
from datetime import date,datetime, timedelta
import json
import random
import string
import hashlib
import os
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.hashers import make_password


currentDate = datetime.now().strftime("%Y-%m-%d")
currentTime =  datetime.now().strftime('%H:%M:%S')

def get_MD5(Password):
	md5 = hashlib.md5()
	md5.update(Password.encode('utf-8'))
	return md5.hexdigest()


# Create your views here.
def sys_admin_home(request):
	dt = datetime.strptime(currentDate, '%Y-%m-%d')
	start = dt - timedelta(days=dt.weekday())
	end = start + timedelta(days=6)
	startDate = start.strftime('%Y-%m-%d')
	endDate = end.strftime('%Y-%m-%d')
	Title ='Admin Home Page'
	if 'Employee_ID' in request.session:
		fourdates = date.today() - timedelta(days=4)
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		CheckIn = ''
		CheckOut = ''
		Marklist = ['off', 'mc']
		CheckValues = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(
			StartDate=currentDate)
		if CheckValues.exists():
			AttenCheck = WorkSchedule.objects.get(Employee_id=request.session['Employee_ID'], StartDate=currentDate)
			if AttenCheck.Mark.lower() != 'off' or AttenCheck.Mark.lower() != 'mc':
				if AttenCheck.InTime is None and AttenCheck.OutTime is not None:
					CheckIn = "Pending"
					CheckOut = AttenCheck.OutTime
				elif AttenCheck.OutTime is None and AttenCheck.InTime is not None:
					CheckIn = AttenCheck.InTime
					CheckOut = "Pending"
				elif AttenCheck.InTime is None and AttenCheck.OutTime is None:
					CheckOut = "Pending"
					CheckIn = "Pending"
				else:
					CheckIn = AttenCheck.InTime
					CheckOut = AttenCheck.OutTime
			else:
				CheckIn = 'OFF'
				CheckOut = 'OFF'

		scheduleWeek = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'], StartDate__lte=endDate,
												   StartDate__gte=startDate,StartTime__isnull=False,EndTime__isnull=False).order_by('StartDate')

		CountAsent = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 StartDate__lte=currentDate, StartDate__gte=startDate).filter(Mark='Absent').count()

		RecentData = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 StartDate__lte=currentDate).order_by("StartDate")



		context = {
			'Role': currentEmployee.Role.Role_ID,
			'Employee_ID': currentEmployee.Employee_ID,
			'Full_Name': currentEmployee.Full_Name,
			'Job_Title': currentEmployee.Job_Title,
			'PFP': currentEmployee.Profile_Image.url,
			'Redata': RecentData,
			'ScheduleWeek': scheduleWeek,
			'count':CountAsent,
			'CheckIn': CheckIn,
			'CheckOut': CheckOut,
			'title':Title,
		}

		return render(request, 'sys_admin/sys_admin_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def sys_admin_view_employees(request):

	currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
	Title ='Admin View Employees Page'
	allEmployees = Employee.objects.all()
	context={
		'Employee_ID' : currentEmployee.Employee_ID,
		'Full_Name' : currentEmployee.Full_Name,
		'Role' : currentEmployee.Role.Role_Name,
		'PFP' : currentEmployee.Profile_Image.url,
		'Employees' : allEmployees,
		'title': Title,
	}

	return render(request, 'sys_admin/sys_admin_view_employees.html', context)



def sys_admin_create_user(request):
	BigEmployess = Employee.objects.all().order_by('Employee_ID').last()

	if request.method == 'POST':
		New_Employee_Full_Name = request.POST.get('name')
		New_Employee_Job_Title = request.POST.get('Job_title')
		New_Employee_ID = request.POST.get('EmployeeID')
		New_Phone_Number = request.POST.get('phone')
		New_Email_Address = request.POST.get('email')
		New_Role_Name = request.POST.get('roles')

		# do password hash later
		New_Password = request.POST.get('newPassword')
		New_Password_2 = request.POST.get('renewPassword')
		Random_salt = ''.join(random.sample(string.ascii_letters + string.digits+string.punctuation, 4))
		New_salt=Random_salt
		print(New_Password+New_salt)
		Encry_Pass = get_MD5(New_Password+New_salt)
		print(Encry_Pass)


		#if employee_ID is taken

		if Employee.objects.filter(Employee_ID=New_Employee_ID).exists():
			messages.error(request, 'There already exist such Employee ID')
			return redirect('sys_admin_create_user')

		elif New_Password != New_Password_2:
			messages.error(request, 'Your passwords does not match')
			return redirect('sys_admin_create_user')
		else:
			New_Role = Role.objects.get(Role_Name=New_Role_Name)

			# if have PFP

			if request.FILES.get('profilepic') is not None:
				New_PFP = request.FILES['profilepic']
				new_employee = Employee(Employee_ID=New_Employee_ID, Full_Name=New_Employee_Full_Name, Phone_Number=New_Phone_Number,
									 Email_Address=New_Email_Address, Role=New_Role,salt=New_salt, Job_Title=New_Employee_Job_Title,Start_Date=currentDate ,Password=Encry_Pass, Profile_Image=New_PFP)
			else:
				new_employee = Employee(Employee_ID=New_Employee_ID, Full_Name=New_Employee_Full_Name, Phone_Number=New_Phone_Number,Start_Date=currentDate,
									 Email_Address=New_Email_Address, Job_Title=New_Employee_Job_Title, salt=New_salt,Role=New_Role, Password=Encry_Pass,Profile_Image='profile_pics/default.jpg')
			new_employee.save()
			messages.success(request, 'New account has been created')
			return redirect('sys_admin_create_user')

	else:
		Title ='Create Account'
		context = {
			'BigEmpid': BigEmployess.Employee_ID + 1,
			'title': Title,
		}
		return render(request, 'sys_admin/sys_admin_create_user.html',context)


def delete_employee(request, delete_employee_id):
	if Employee.objects.filter(Employee_ID=delete_employee_id).count() == 1:
		Employee_to_delete = Employee.objects.get(Employee_ID=delete_employee_id)
		Employee_to_delete.delete()

	return redirect('sys_admin_view_employees')


def user_profile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if request.FILES.get('Pic') is not None:
					New_p = request.FILES['Pic']
					if currentEmployee.Profile_Image != 'media/profile_pics/default.jpg':
						if os.path.isfile(currentEmployee.Profile_Image.path):
							os.remove(currentEmployee.Profile_Image.path)

					currentEmployee.Profile_Image = New_p
				else:
					currentEmployee.Profile_Image = 'media/profile_pics/default.jpg'
				currentEmployee.Full_Name = request.POST.get('fullName_edit')
				currentEmployee.Phone_Number = request.POST.get('phone_edit')
				currentEmployee.Email_Address = request.POST.get('email_edit')
				currentEmployee.save()

				return redirect('sys_admin_user_profile')

			# for change password form
			elif request.POST.get('form_type') == 'changePassword':

				Random_salt = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 4))
				New_salt = Random_salt
				old_Password = request.POST.get('password')
				new_passWord = request.POST.get('newpassword')
				new_password_2 = request.POST.get('renewpassword')
				Update_pssword = get_MD5(new_passWord + New_salt)
				old_pss = get_MD5(old_Password + currentEmployee.salt)
				if new_passWord == new_password_2 and old_pss == currentEmployee.Password:
					currentEmployee.Password = Update_pssword
					currentEmployee.salt = New_salt
					currentEmployee.save()
					messages.info(request, 'Your password has been changed')
					return redirect('sys_admin_user_profile')
				elif new_passWord != new_password_2:
					messages.info(request, 'password is different')
					return redirect('sys_admin_user_profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('sys_admin_user_profile')



		else:
			Title='User Profile'
			context = {
				'Employee_ID' : currentEmployee.Employee_ID,
				'Full_Name' : currentEmployee.Full_Name,
				'Role' : currentEmployee.Role.Role_Name,
				'Email' : currentEmployee.Email_Address,
				'Phone' : currentEmployee.Phone_Number,
				'PFP' : currentEmployee.Profile_Image.url,
				'title': Title,
			}
			return render(request, 'sys_admin/sys_admin_user_profile.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')



def edit_employee(request, edit_employee_id):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		if request.method == 'POST':
			if request.POST.get('form_type')=='editProfile':
				edit_employee = Employee.objects.get(Employee_ID=edit_employee_id)
				if request.FILES.get('Pic') is not None:
					New_p = request.FILES['Pic']
					if currentEmployee.Profile_Image != 'media/profile_pics/default.jpg':
						if os.path.isfile(currentEmployee.Profile_Image.path):
							os.remove(currentEmployee.Profile_Image.path)

					edit_employee.Profile_Image =New_p
				else:
					currentEmployee.Profile_Image= 'media/profile_pics/default.jpg'
				edit_employee.Full_Name = request.POST.get('fullName')
				edit_employee.Phone_Number = request.POST.get('phone')
				edit_employee.Email_Address = request.POST.get('email')

				edit_employee.save()

				return redirect('/sys_admin/view_employees/edit/' + str(edit_employee_id))

			elif request.POST.get('form_type') == 'changePassword':
				edit_employee = Employee.objects.get(Employee_ID=edit_employee_id)
				Random_salt = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 4))
				New_salt = Random_salt
				new_passWord = request.POST.get('newpassword')
				new_password_2 = request.POST.get('renewpassword')
				Update_pssword = get_MD5(new_passWord + New_salt)

				if new_passWord == new_password_2:
					edit_employee.Password = Update_pssword
					edit_employee.salt = New_salt
					edit_employee.save()
					messages.info(request, 'Your password has been changed')
					return redirect('/sys_admin/view_employees/edit/' + str(edit_employee_id))
				elif new_passWord!=new_password_2:
					messages.info(request, 'password is different')
					return redirect('/sys_admin/view_employees/edit/' + str(edit_employee_id))

		else:
			Title='Edit Employee Page'
			if Employee.objects.filter(Employee_ID=edit_employee_id).count() == 1:
				edit_employee = Employee.objects.get(Employee_ID=edit_employee_id)
				context = {
					'edit_employee_id' : edit_employee_id,
					'edit_employee_full_name' : edit_employee.Full_Name,
					'edit_employee_role' : edit_employee.Role,
					'edit_employee_phone' : edit_employee.Phone_Number,
					'edit_employee_email' : edit_employee.Email_Address,
					'edit_employee_pfp' : edit_employee.Profile_Image.url,
					'Full_Name' : currentEmployee.Full_Name,
					'Role' : currentEmployee.Role.Role_Name,
					'PFP' : currentEmployee.Profile_Image.url,
					'title': Title,
				}

			return render(request, 'sys_admin/sys_admin_edit_employee.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')

def schedule(request):
	if 'Employee_ID' in request.session:
		# template = loader.get_template('HR/schedule.html')
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		data = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(StartDate__isnull=False,StartTime__isnull=False,EndTime__isnull=False)
		js_data =serializers.serialize('json',data,fields=['StartDate','EndDate','StartTime','EndTime'])
		json_data=json.loads(js_data)
		for d in json_data:
			del d['pk']
			del d['model']
		Title="Schedule Page"
		js_data = json.dumps(json_data,ensure_ascii=False)
		context = {
			'Employee_ID' : currentEmployee.Employee_ID,
			'Job_Title' : currentEmployee.Job_Title,
			'Full_Name' : currentEmployee.Full_Name,
			'PFP': currentEmployee.Profile_Image.url,
			'js_data': js_data,
			'title': Title,
		}

		return render(request, 'sys_admin/sys_admin_schedule.html',context)
		# return HttpResponse(template.render(context, request))
	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def upload_img(request, empid):
	if 'Employee_ID' in request.session:
		Emp = Employee.objects.filter(Employee_ID=empid)

		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		if request.method == 'POST':
			filepath = os.path.join(settings.BASE_DIR, 'media', 'verify', str(empid))
			if not os.path.exists(filepath):
				for f in request.FILES.getlist('UploadImage'):

					print(f.name)
			# for root,dirs,files in os.walk(os.getcwd):
			# 	for i in New_p:
			# 		print(root,dirs)

			return redirect('/sys_admin/view_employees/edit/' + str(empid))
		elif Emp.exists():
			Information={
				'Name':Emp[0].Full_Name,
				"Emplid":Emp[0].Employee_ID,
			}

			return render(request, 'sys_admin/sys_admin_upload_img.html',Information)


def logout(request):
	request.session.flush()
	messages.info(request, 'You have been logged out')
	return redirect('login')
