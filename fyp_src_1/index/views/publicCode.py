from ..models import Employee,Role,WorkSchedule
from datetime import date,datetime, timedelta
currentDate = datetime.now().strftime("%Y-%m-%d")
import schedule
#pip install schedule
import time
from django.db.models import Q


def updateMark():
	UserStatus = WorkSchedule.objects.filter(StartDate__lt=currentDate)
	print(UserStatus)
	for i in UserStatus:
		WorksId = WorkSchedule.objects.get(WorkSchedule_id=i.WorkSchedule_id)
		if WorksId.Mark.lower()!='off' or WorksId.Mark.lower()!='mc':
			if  WorksId.InTime=='' or WorksId.InTime is None or WorksId.OutTime is None or WorksId.OutTime=='':
				WorksId.Mark ='Absent'

			elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
				WorksId.Mark='Late & leave early'

			elif WorksId.StartTime >= WorksId.InTime and WorksId.EndTime > WorksId.OutTime:
				WorksId.Mark='leave early'

			elif WorksId.StartTime < WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
				WorksId.Mark='late'

			elif WorksId.StartTime >= WorksId.InTime and WorksId.EndTime <= WorksId.OutTime:
				WorksId.Mark = 'Present'

			else:
				WorksId.Mark='Pending'
			WorksId.save()



schedule.every().hour.do(updateMark)

while True:
	schedule.run_pending()   # 运行所有可以运行的任务
	time.sleep(10)

