import json
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ..models import Employee, Role, WorkSchedule
from django.contrib import messages
from django.core import serializers
from datetime import date, datetime, timedelta
import os
import hashlib
import random
import string

currentDate = datetime.now().strftime("%Y-%m-%d")
currentTime = datetime.now().strftime('%H:%M:%S')


def CheckMark():
    UserStatus = WorkSchedule.objects.filter(StartDate__lt=currentDate)
    for i in UserStatus:
        WorksId = WorkSchedule.objects.get(WorkSchedule_id=i.WorkSchedule_id)
        if WorksId.Mark != 'Off' and WorksId.Mark != 'MC':
            if WorksId.InTime is None and WorksId.StartTime is not None or WorksId.OutTime is None and WorksId.EndTime is not None:
                WorksId.Mark = 'Absent'
                WorksId.save()
            elif WorksId.InTime is not None and WorksId.StartTime is not None or WorksId.OutTime is not None and WorksId.EndTime is not None:
                if WorksId.StartTime >= WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
                    WorksId.Mark = 'Present'
                    WorksId.save()
                elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
                    WorksId.Mark = 'Late & leave early'
                    WorksId.save()
                elif WorksId.StartTime >= WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
                    WorksId.Mark = 'Leave early'
                    WorksId.save()
                elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
                    WorksId.Mark = 'Late'
                    WorksId.save()
    current = WorkSchedule.objects.filter(StartDate=currentDate)
    for k in current:
        userid = WorkSchedule.objects.get(WorkSchedule_id=k.WorkSchedule_id)
        if userid.Mark != 'Off' and userid.Mark != 'MC':
            if userid.InTime is not None and userid.OutTime is not None:
                if userid.StartTime >= userid.InTime and userid.EndTime <= userid.OutTime:
                    userid.Mark = 'Present'
                    userid.save()
                elif userid.StartTime < userid.InTime and userid.EndTime > userid.OutTime:
                    userid.Mark = 'Late & leave early'
                    userid.save()
                elif userid.StartTime >= userid.InTime and userid.EndTime > userid.OutTime:
                    userid.Mark = 'Leave early'
                    userid.save()
                elif userid.StartTime < userid.InTime and userid.EndTime <= userid.OutTime:
                    userid.Mark = 'Late'
                    userid.save()


def get_MD5(Password):
    md5 = hashlib.md5()
    md5.update(Password.encode('utf-8'))
    return md5.hexdigest()


def HR_home(request):
    CheckMark()
    dt = datetime.strptime(currentDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    startDate = start.strftime('%Y-%m-%d')
    endDate = end.strftime('%Y-%m-%d')
    Title = 'HR Home Page'
    if 'Employee_ID' in request.session:
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
        CheckIn = ''
        CheckOut = ''

        CheckValues = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(
            StartDate=currentDate)
        if CheckValues.exists():
            AttenCheck = WorkSchedule.objects.get(Employee_id=request.session['Employee_ID'], StartDate=currentDate)
            if AttenCheck.Mark.lower() == 'pending':
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
                                                   StartDate__gte=startDate, StartTime__isnull=False,
                                                   EndTime__isnull=False).order_by('StartDate')

        CountAsent = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'], StartDate__lte=currentDate,
                                                 StartDate__gte=startDate).filter(Mark='Absent').count()

        RecentData = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID'],
                                                 StartDate__lte=currentDate).order_by('-StartDate')

        context = {
            'Role': currentEmployee.Role.Role_ID,
            'Employee_ID': currentEmployee.Employee_ID,
            'Full_Name': currentEmployee.Full_Name,
            'Job_Title': currentEmployee.Job_Title,
            'PFP': currentEmployee.Profile_Image.url,
            'Redata': RecentData,
            'count': CountAsent,
            'ScheduleWeek': scheduleWeek,
            'CheckIn': CheckIn,
            'CheckOut': CheckOut,
            'title': Title,
        }
        return render(request, 'HR/HR_home.html', context)
    else:
        messages.error(request, 'Please login first')
        return redirect('login')


def HR_Profile(request):
    if 'Employee_ID' in request.session:
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
        Title = 'User Profile'
        if request.method == 'POST':
            # for edit user profile form
            if request.POST.get('form_type') == 'editProfile':

                if request.FILES.get('Pic') is not None:
                    New_p = request.FILES['Pic']
                    if currentEmployee.Profile_Image != 'profile_pics/default.jpg':

                        if os.path.isfile(currentEmployee.Profile_Image.path):
                            os.remove(currentEmployee.Profile_Image.path)

                    currentEmployee.Profile_Image = New_p
                else:
                    currentEmployee.Profile_Image = 'profile_pics/default.jpg'

                currentEmployee.Full_Name = request.POST.get('fullName_edit')
                currentEmployee.Phone_Number = request.POST.get('phone')
                currentEmployee.Email_Address = request.POST.get('email')
                currentEmployee.save()

                return redirect('HR_Profile')

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
                    return redirect('HR_Profile')
                elif new_passWord != new_password_2:
                    messages.info(request, 'password is different')
                    return redirect('HR_Profile')

                else:
                    messages.error(request, 'Your current password does not match')
                    return redirect('HR_Profile')

        else:
            context = {
                'Employee_ID': currentEmployee.Employee_ID,
                'Full_Name': currentEmployee.Full_Name,
                'Role': currentEmployee.Role.Role_Name,
                'Email': currentEmployee.Email_Address,
                'Phone': currentEmployee.Phone_Number,
                'Job_Title': currentEmployee.Job_Title,
                'PFP': currentEmployee.Profile_Image.url,
                'title': Title,
            }
            return render(request, 'HR/HR_profile.html', context)
    else:
        messages.error(request, 'Please login')
        return redirect('login')


def HR_EmployeePage(request):
    currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
    Title = 'Employees Page'
    data = Employee.objects.all()
    context = {
        'Employee_ID': currentEmployee.Employee_ID,
        'Job_Title': currentEmployee.Job_Title,
        'Full_Name': currentEmployee.Full_Name,
        'PFP': currentEmployee.Profile_Image.url,
        'data': data,
        'title': Title,
    }
    return render(request, 'HR/employees.html', context)


def HR_EmpProfile(request, Empid):
    if 'Employee_ID' in request.session:
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

        Title = 'HR-Employee Profile'
        EmpCheck = Employee.objects.filter(Employee_ID=Empid)

        if EmpCheck.exists():
            Myinfo = Employee.objects.get(Employee_ID=Empid)
            context = {
                'Role': currentEmployee.Role.Role_ID,
                'Employee_ID': currentEmployee.Employee_ID,
                'Full_Name': currentEmployee.Full_Name,
                'Job_Title': currentEmployee.Job_Title,
                'PFP': currentEmployee.Profile_Image.url,
                'Emp_id': Myinfo.Employee_ID,
                'Emp_FullName': Myinfo.Full_Name,
                'Emp_JobTitle': Myinfo.Job_Title,
                'Emp_Email': Myinfo.Email_Address,
                'Emp_Phone': Myinfo.Phone_Number,
                'Emp_PFP': Myinfo.Profile_Image.url,
                'Emp_Role': Myinfo.Role.Role_Name,
                'title': Title,
            }
            return render(request, 'HR/employees-profile.html', context)


def HR_View_Schedule(request):
    if 'Employee_ID' in request.session:
        # template = loader.get_template('HR/schedule.html')
        Title = 'View Schedule'
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
        data = WorkSchedule.objects.filter(Employee_id=request.session['Employee_ID']).filter(StartDate__isnull=False,
                                                                                              StartTime__isnull=False,
                                                                                              EndTime__isnull=False)
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
            'title': Title,
            'js_data': js_data,
        }

        return render(request, 'HR/schedule.html', context)
    # return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'Please login first')
        return redirect('login')


def Change_Status(request, Empid, Wid):
    if 'Employee_ID' in request.session:
        Title = 'Change Employee Work Stauts'
        sdate = datetime.now() + timedelta(days=3)
        currentDate = sdate.strftime("%Y-%m-%d")
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])

        Emp = Employee.objects.get(Employee_ID=Empid)
        Atten = WorkSchedule.objects.filter(Employee_id=Empid, WorkSchedule_id=Wid)
        if request.method == 'POST':
            UpdateAttendance = WorkSchedule.objects.get(WorkSchedule_id=Wid)
            NewStatus = request.POST.get('status')

            Mc = 'MC'
            if NewStatus == 'Pending':
                UpdateAttendance.Mark = NewStatus
                UpdateAttendance.StartTime = request.POST.get('timestartnew')
                UpdateAttendance.EndTime = request.POST.get('timeendnew')
                UpdateAttendance.save()
            elif NewStatus == Mc:
                UpdateAttendance.Mark = NewStatus
                UpdateAttendance.save()
            else:
                UpdateAttendance.Mark = NewStatus
                UpdateAttendance.StartTime = None
                UpdateAttendance.EndTime = None
                UpdateAttendance.save()

            CheckMark()
            return redirect('EmployeeSchedule', Editempid=Empid)
        else:
            context = {
                'Role': currentEmployee.Role.Role_ID,
                'Employee_ID': currentEmployee.Employee_ID,
                'Full_Name': currentEmployee.Full_Name,
                'Job_Title': currentEmployee.Job_Title,
                'PFP': currentEmployee.Profile_Image.url,
                "Emp_id": Emp.Employee_ID,
                'Name': Emp.Full_Name,
                'Data': Atten,
                'title': Title,
            }
            return render(request, 'HR/change-status.html', context)


def Employee_View_Schedule(request, Editempid):
    if 'Employee_ID' in request.session:
        Title = 'Employee Attendance Page'
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
        Emp = Employee.objects.get(Employee_ID=Editempid)
        Emp_Atten = WorkSchedule.objects.filter(Employee_id=Editempid).order_by('StartDate')[:60]

        context = {
            'Employee_ID': currentEmployee.Employee_ID,
            'Job_Title': currentEmployee.Job_Title,
            'PFP': currentEmployee.Profile_Image.url,
            'Full_Name': currentEmployee.Full_Name,
            "Emp_id": Emp.Employee_ID,
            'Name': Emp.Full_Name,
            'AttenData': Emp_Atten,
            'title': Title,
        }

        return render(request, 'HR/employees-view-schedule.html', context)


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


def alldays(year, month, Inputday, whichDayYouWant):
    d = date(year, month, Inputday)
    d += timedelta(days=(weeknum(whichDayYouWant) - d.weekday()))
    while d.month == month:
        yield d
        d += timedelta(days=7)


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def Emp_update_Schedule(request, Editempid):
    Title = 'Upload Schedule'
    if 'Employee_ID' in request.session:
        currentEmployee = Employee.objects.get(Employee_ID=request.session['Employee_ID'])
        Emp = Employee.objects.get(Employee_ID=Editempid)
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        currenDay = datetime.now().day

        if request.method == "POST":
            SchedduleYear = request.POST.get('yearselect')
            SchedduleMonth = request.POST.get('monthselect')

            StartTime = ''
            EndTime = ''

            for weeks in weekdays:
                Marks = request.POST.get(str(weeks))
                if Marks != 'Pending':
                    StartTime = None
                    EndTime = None
                else:
                    StartTime = request.POST.get('timestart')
                    EndTime = request.POST.get('timeend')

                if currentYear < int(SchedduleYear) or int(SchedduleMonth) > currentMonth:
                    for d in alldays(int(SchedduleYear), int(SchedduleMonth), 1, weeks):
                        WordSche = WorkSchedule(StartDate=d, StartTime=StartTime, EndTime=EndTime,
                                                Employee_id=Editempid, Mark=Marks)
                        WordSche.save()
                else:
                    for d in alldays(currentYear, currentMonth, currenDay, weeks):
                        Start = WorkSchedule.objects.filter(Employee_id=Editempid, StartDate=d)
                        if Start.exists():
                            WorkId = WorkSchedule.objects.get(Employee_id=Editempid, StartDate=d)
                            UpdateWork = WorkSchedule.objects.get(WorkSchedule_id=WorkId.WorkSchedule_id)
                            UpdateWork.StartTime = StartTime
                            UpdateWork.EndTime = EndTime
                            UpdateWork.Mark = Marks
                            UpdateWork.save()

                        else:
                            Marks = request.POST.get(str(weeks))
                            WordSche = WorkSchedule(StartDate=d, StartTime=StartTime, EndTime=EndTime,
                                                    Employee_id=Editempid, Mark=Marks)
                            WordSche.save()

                CheckMark()

            return redirect('EmployeesPage')
        else:
            context = {
                'Employee_ID': currentEmployee.Employee_ID,
                'Job_Title': currentEmployee.Job_Title,
                'Full_Name': currentEmployee.Full_Name,
                'PFP': currentEmployee.Profile_Image.url,
                "Emp_id": Emp.Employee_ID,
                'Name': Emp.Full_Name,
                'title': Title,
            }
        return render(request, 'HR/upload-schedule.html', context)
