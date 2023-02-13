from django.shortcuts import render, redirect
from index.models import Employee, Role,WorkSchedule
from django.contrib import messages
import os
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import date,datetime, timedelta
from django.core import serializers
import json
import hashlib
import random
import string

import os


def get_MD5(Password):
	md5 = hashlib.md5()
	md5.update(Password.encode('utf-8'))
	return md5.hexdigest()

currentDate = datetime.now().strftime("%Y-%m-%d")
currentTime =  datetime.now().strftime('%H:%M:%S')

def Employee_home(request):
	dt = datetime.strptime(currentDate, '%Y-%m-%d')
	start = dt - timedelta(days=dt.weekday())
	end = start + timedelta(days=6)
	startDate = start.strftime('%Y-%m-%d')
	endDate = end.strftime('%Y-%m-%d')
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
		scheduleWeek = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'], StartDate__lte=endDate,StartDate__gte=startDate).exclude(Mark__in=Marklist).order_by('StartDate')

		CountAsent = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 StartDate__lte=currentDate, StartDate__gte=startDate).filter(Mark='Absent').count()
		RecentData = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 StartDate__lte=currentDate).exclude(Mark__in=Marklist).order_by('StartDate')

		context = {
			'Role': currentEmployee.Role.Role_ID,
			'Employee_ID': currentEmployee.Employee_ID,
			'Full_Name': currentEmployee.Full_Name,
			'Job_Title': currentEmployee.Job_Title,
			'PFP': currentEmployee.Profile_Image.url,
			'Redata': RecentData,
			'ScheduleWeek': scheduleWeek,
			'count': CountAsent,
			'CheckIn': CheckIn,
			'CheckOut': CheckOut,
		}
		return render(request, 'employee/employee_home.html', context)


	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def Employee_schedule(request):
	if 'Employee_ID' in request.session:
		# template = loader.get_template('HR/schedule.html')
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		data = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'])
		js_data = serializers.serialize('json', data, fields=['StartDate', 'StartTime', 'EndTime'])
		json_data = json.loads(js_data)
		for d in json_data:
			del d['pk']
			del d['model']

		js_data = json.dumps(json_data, ensure_ascii=False)
		context = {
			'Employee_ID': currentEmployee.Employee_ID,
			'Job_Title': currentEmployee.Job_Title,
			'Full_Name': currentEmployee.Full_Name,
			'PFP': currentEmployee.Profile_Image.url,
			'js_data': js_data,
		}

		return render(request, 'employee/schedule.html',context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def viewProfile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if request.FILES.get('Pic') is not None:
					New_p = request.FILES['Pic']
					if currentEmployee.Profile_Image:
						if os.path.isfile(currentEmployee.Profile_Image.path):
							os.remove(currentEmployee.Profile_Image.path)

					currentEmployee.Profile_Image = New_p

				currentEmployee.Full_Name = request.POST.get('fullName_edit')
				currentEmployee.Phone_Number = request.POST.get('phone')
				currentEmployee.Email_Address = request.POST.get('email')

				currentEmployee.save()

				return redirect('Profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':
				Random_salt = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 4))
				New_salt = Random_salt
				old_Password = request.POST.get('password')
				new_passWord =request.POST.get('newpassword')
				new_password_2 =request.POST.get('renewpassword')
				Update_pssword = get_MD5(new_passWord+New_salt)
				old_pss = get_MD5(old_Password + currentEmployee.salt)
				if new_passWord ==new_password_2 and old_pss == currentEmployee.Password:
					currentEmployee.Password = Update_pssword
					currentEmployee.salt=New_salt
					currentEmployee.save()
					messages.info(request, 'Your password has been changed')
					return redirect('Profile')
				elif new_passWord != new_password_2:
					messages.info(request, 'password is different')
					return redirect('Profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('Profile')



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
			return render(request, 'employee/users_profile.html', context)
	else:
		messages.error(request, 'Please login')
		return redirect('login')



