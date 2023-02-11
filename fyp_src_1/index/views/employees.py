from django.shortcuts import render, redirect
from index.models import Employee, Role,WorkSchedule
from django.contrib import messages
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import date,datetime, timedelta
from django.core import serializers
import json

currentDate = datetime.now().strftime("%Y-%m-%d")
currentTime =  datetime.now().strftime('%H:%M:%S')

def Employee_home(request):
	dt = datetime.strptime(currentDate, '%Y-%m-%d')
	start = dt - timedelta(days=dt.weekday() + 1)
	end = start + timedelta(days=6)
	startDate = start.strftime('%Y-%m-%d')
	endDate = end.strftime('%Y-%m-%d')
	if 'Employee_ID' in request.session:
		fourdates = date.today() - timedelta(days=4)
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		CheckIn = ''
		CheckOut = ''
		Marklist = ['off', 'mc']
		try:
			currentAtten = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(Q(AttendanDate=currentDate)|Q(StartDate=currentDate))

			if currentAtten.Mark.lower() != 'off' or currentAtten.Mark.lower() != 'mc':
				CheckIn = currentAtten.InTime
				CheckOut = currentAtten.OutTime
			else:
				CheckIn = 'OFF'
				CheckOut='OFF'
		except (AttributeError,ObjectDoesNotExist):
			CheckIn = 'Waiting'
			CheckOut = 'Waiting'

		scheduleWeek = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'], StartDate__lte=endDate,StartDate__gte=startDate).exclude(Mark__in=Marklist).order_by('StartDate')

		CountAsent = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 AttendanDate__lte=currentDate, AttendanDate__gte=startDate).filter(Mark='Absent').count()
		RecentData = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
												 AttendanDate__lte=currentDate).exclude(Mark__in=Marklist).order_by(
			'AttendanDate', 'EndDate')

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
	# posts = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'], AttendanDate__gte=(now-timedelta(days=5)).date()).values("WorkSchedule_id")

	# if WorkSchedule.objects.filter(StartDate=currentDate,AttendanDate=currentDate).exists():
	# 	print("yes")
		return render(request, 'employee/employee_home.html', context)


	else:
		messages.error(request, 'Please login first')
		return redirect('login')

def Employee_schedule(request):
	if 'Employee_ID' in request.session:
		# template = loader.get_template('HR/schedule.html')
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		data = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'])
		js_data = serializers.serialize('json', data, fields=['StartDate', 'EndDate', 'StartTime', 'EndTime'])
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

				if Role.objects.filter(Role_Name=request.POST.get('role_edit')) == 0:
					messages.error(request, 'No such role')
					return redirect('Profile')


				currentEmployee.Full_Name = request.POST.get('fullName_edit')

				currentEmployee.Phone_Number = request.POST.get('phone')
				currentEmployee.Email_Address = request.POST.get('email')


				currentEmployee.save()

				return redirect('Profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':

				# make sure current password matches
				if request.POST.get('password') == currentEmployee.Password:
					currentEmployee.Password = request.POST.get('newpassword')
					currentEmployee.save()

					messages.info(request, 'Your password has been changed')
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

