import json


from django.shortcuts import render, redirect
from index.models import Employee, Role,WorkSchedule
from django.contrib import messages
from django.template import loader
from django.db.models.functions import Extract
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from datetime import date,datetime, timedelta



def HR_home(request):
	if 'Employee_ID' in request.session:
		currentDate = datetime.now().strftime("%Y-%m-%d")
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		RecentData = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(AttendanDate__lte=currentDate).order_by('AttendanDate','EndDate')
		AttendanceData = WorkSchedule.objects.filter(Employee_id= request.session['Employee_ID']).filter(AttendanDate__lte=currentDate)[:5]
		context = {
			'Role' : currentEmployee.Role.Role_ID,
			'Employee_ID' : currentEmployee.Employee_ID,
			'Full_Name' : currentEmployee.Full_Name,
			'Job_Title' : currentEmployee.Job_Title,
			'PFP' : currentEmployee.Profile_Image.url,
			'Redata': RecentData,
			'data':AttendanceData,
		}

		return render(request, 'HR/HR_home.html', context)

	else:
		messages.error(request, 'Please login first')
		return redirect('login')


def HR_Profile(request):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

		if request.method == 'POST':
			# for edit user profile form
			if request.POST.get('form_type') == 'editProfile':

				if Role.objects.filter(Role_Name=request.POST.get('role_edit')) == 0:
					messages.error(request, 'No such role')
					return redirect('HR_Profile')


				currentEmployee.Full_Name = request.POST.get('fullName_edit')

				currentEmployee.Phone_Number = request.POST.get('phone')
				currentEmployee.Email_Address = request.POST.get('email')


				currentEmployee.save()

				return redirect('HR_Profile')

			# for change password form	
			elif request.POST.get('form_type') == 'changePassword':

				# make sure current password matches
				if request.POST.get('password') == currentEmployee.Password:
					currentEmployee.Password = request.POST.get('newpassword')
					currentEmployee.save()

					messages.info(request, 'Your password has been changed')
					return redirect('HR_Profile')

				else:
					messages.error(request, 'Your current password does not match')
					return redirect('HR_Profile')


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
			return render(request, 'HR/HR_profile.html', context)
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
	return redirect('HR_Profile')


def HR_EmployeePage(request):
	currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
	data = Employee.objects.all()
	context = {
		'Employee_ID' : currentEmployee.Employee_ID,
		'Job_Title' : currentEmployee.Job_Title,
		'Full_Name' : currentEmployee.Full_Name,
		'data': data,
	}
	return render(request, 'HR/employees.html', context)


def HR_EmpProfile(request):
	if request.method == 'GET':
		EmpId = request.GET.get('id')
		# print(EmpId,"testes")
		
		Myinfo = Employee.objects.get(Employee_ID = EmpId)
		context = {
			'Employee_ID': Myinfo.Employee_ID,
			'Full_Name': Myinfo.Full_Name,
			'Role': Myinfo.Role.Role_Name,
			'Job_Title' : Myinfo.Job_Title,
			'Email' : Myinfo.Email_Address,
			'Phone' : Myinfo.Phone_Number,
			'PFP' : Myinfo.Profile_Image.url,
		}
		return render(request, 'HR/employees-profile.html', context)
	# return HttpResponse(EmpId)


def HR_View_Schedule(request):
	if 'Employee_ID' in request.session:
		# template = loader.get_template('HR/schedule.html')
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		data = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'])
		js_data =serializers.serialize('json',data,fields=['StartDate','EndDate','StartTime','EndTime'])
		json_data=json.loads(js_data)
		for d in json_data:
			del d['pk']
			del d['model']

		js_data = json.dumps(json_data,ensure_ascii=False)
		context = {
			'Employee_ID' : currentEmployee.Employee_ID,
			'Job_Title' : currentEmployee.Job_Title,
			'Full_Name' : currentEmployee.Full_Name,
			'PFP': currentEmployee.Profile_Image.url,
			'js_data': js_data,
		}

		return render(request, 'HR/schedule.html',context)
		# return HttpResponse(template.render(context, request))
	else:
		messages.error(request, 'Please login first')
		return redirect('login')



def Change_Status(request, Editempid):
	if 'Employee_ID' in request.session:
		currentDate = datetime.now().strftime("%Y-%m-%d")
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		Emp = Employee.objects.get(Employee_ID=Editempid)
		Atten = WorkSchedule.objects.filter(Employee_id=Editempid).filter(AttendanDate__lte=currentDate)
		if request.method=='POST':
			print('yeas')
			Aid = request.POST.get('dateselected')
			UpdateAttendance = WorkSchedule.objects.get(WorkSchedule_id=request.POST.get('dateselected'))
			NewStatus =request.POST.get('status')
			StatusName ='worktime'
			if NewStatus == StatusName:
				UpdateAttendance.Mark = NewStatus
				UpdateAttendance.InTime =request.POST.get('timestartnew')
				UpdateAttendance.OutTime =request.POST.get('timeendnew')
				UpdateAttendance.save()
			else:
				UpdateAttendance.Mark = NewStatus
				UpdateAttendance.save()
			return redirect('EmployeesPage')
		else:
			context={
				'Role': currentEmployee.Role.Role_ID,
				'Employee_ID': currentEmployee.Employee_ID,
				'Full_Name': currentEmployee.Full_Name,
				'Job_Title': currentEmployee.Job_Title,
				'PFP': currentEmployee.Profile_Image.url,
				"Emp_id" :Emp.Employee_ID,
				'Name' : Emp.Full_Name,
				'Data':Atten,
			}
			return render(request, 'HR/change-status.html',context)




def Employee_View_Schedule(request,Editempid):

	if 'Employee_ID' in request.session:
		currentDate = datetime.now().strftime("%Y-%m-%d")
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		Emp = Employee.objects.get(Employee_ID=Editempid)
		Emp_Atten = WorkSchedule.objects.filter(Employee_id=Editempid,AttendanDate__lte=currentDate).order_by('AttendanDate')


		context={
		'Employee_ID': currentEmployee.Employee_ID,
		'Job_Title': currentEmployee.Job_Title,
		'Full_Name': currentEmployee.Full_Name,
		"Emp_id" :Emp.Employee_ID,
		'Name' : Emp.Full_Name,
		'AttenData':Emp_Atten,
		}

		return render(request, 'HR/employees-view-schedule.html',context)

def weeknum(dayname):
	if dayname == 'Monday':
		return 7
	if dayname == 'Tuesday':
		return 1
	if dayname == 'Wednesday':
		return 2
	if dayname == 'Thursday':
		return 3
	if dayname == 'Friday':
		return 4
	if dayname == 'Saturday':
		return 5
	if dayname == 'Sunday':
		return 6
def alldays(year,month,Inputday,whichDayYouWant):
	d = date(year,month,Inputday)
	d += timedelta(days = (weeknum(whichDayYouWant) - d.weekday()))
	while d.month == month:
		yield d
		d += timedelta(days = 7)

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
def Emp_update_Schedule(request,Editempid):
	if 'Employee_ID' in request.session:
		currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
		Emp = Employee.objects.get(Employee_ID=Editempid)
		currentMonth = datetime.now().month
		currentYear = datetime.now().year
		currenDay = datetime.now().day
		if request.method=="POST":
			SchedduleYear = request.POST.get('yearselect')
			SchedduleMonth =request.POST.get('monthselect')
			StartTime = request.POST.get('timestart')
			EndTime = request.POST.get('timeend')
			if currentYear<int(SchedduleYear) or int(SchedduleMonth)>currentMonth:
				for weeks in weekdays:
					for d in alldays(int(SchedduleYear), int(SchedduleMonth), currenDay, weeks):
						WeeksDay = request.POST.get(str(weeks))
						WordSche = WorkSchedule(StartDate=d,EndDate=d,StartTime=StartTime,EndTime=EndTime,Employee_id=Editempid,Mark=WeeksDay)
						WordSche.save()
			else:
				for weeks in weekdays:
					WeeksDay = request.POST.get(str(weeks))
					for d in alldays(currentYear, currentMonth, currenDay, weeks):
						WordSche = WorkSchedule(StartDate=d,EndDate=d,StartTime=StartTime,EndTime=EndTime,Employee_id=Editempid,Mark=WeeksDay)
						WordSche.save()


			return  redirect('EmployeesPage')
		else:
			context={
			'Employee_ID': currentEmployee.Employee_ID,
			'Job_Title': currentEmployee.Job_Title,
			'Full_Name': currentEmployee.Full_Name,
			"Emp_id" :Emp.Employee_ID,
			'Name' : Emp.Full_Name,
	}
		return render(request, 'HR/upload-schedule.html',context)