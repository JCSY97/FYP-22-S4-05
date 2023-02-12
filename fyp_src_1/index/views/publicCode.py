from ..models import Employee,Role,WorkSchedule
from datetime import date,datetime, timedelta
currentDate = datetime.now().strftime("%Y-%m-%d")
import schedule
#pip install schedule
import time
from django.db.models import Q


def updateMark():
	UserStatus = WorkSchedule.objects.filter(Q(StartDate__lte=currentDate) | Q(AttendanDate__lte=currentDate))
	for i in UserStatus:
		WorksId = WorkSchedule.objects.get(WorkSchedule_id=i.WorkSchedule_id)
		if WorksId.Mark.lower()!='off' or WorksId.Mark.lower()!='mc':
			if  WorksId.InTime=='' or WorksId.InTime is None or WorksId.OutTime is None or WorksId.OutTime=='':
				WorksId.Mark ='Absent'
				WorksId.save()
			elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
				WorksId.Mark='Late & leave early'
				WorksId.save()
			elif WorksId.StartTime >= WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
				WorksId.Mark='leave early'
				WorksId.save()
			elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
				WorksId.Mark='late'
				WorksId.save()
			else:
				WorksId.Mark='Present'
				WorksId.save()


def CheckAtten():
	AllEmpoyee = WorkSchedule.objects.filter(Q(StartDate__lte=currentDate) | Q(AttendanDate__lte=currentDate))
	for d in AllEmpoyee:
		Empid = WorkSchedule.objects.get(WorkSchedule_id=d.WorkSchedule_id)
		if Empid.AttendanDate is None and Empid.StartDate is not None:
			Empid.AttendanDate=Empid.StartDate
			Empid.save()
		elif Empid.StartDate is None or Empid.EndDate is None and Empid.AttendanDate is not None:
			Empid.StartDate =Empid.AttendanDate
			Empid.EndDate = Empid.AttendanDate
			Empid.save()




schedule.every().hour.do(CheckAtten)
schedule.every().hour.do(updateMark)

while True:
	schedule.run_pending()   # 运行所有可以运行的任务
	time.sleep(10)

