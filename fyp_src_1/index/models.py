from django.db import models

# Create your models here.
# all models are to be created in index.models
def user_directory_path(instance, filename): 
	name, ext = filename.split(".")
	name = instance.Employee_ID+"_"+ instance.section
	filename = name +'.'+ ext
	return 'Users_images/{}'.format(filename)


class Role(models.Model):
	Role_ID = models.IntegerField(primary_key=True)
	Role_Name = models.CharField(max_length=100)

	def __str__(self):
		return self.Role_Name

class Employee(models.Model):
	Employee_ID = models.IntegerField(primary_key=True)
	Full_Name = models.CharField(max_length=100)
	Job_Title = models.CharField(max_length=100)
	Phone_Number = models.CharField(max_length=100)
	Email_Address = models.EmailField()
	Role = models.ForeignKey(Role, on_delete=models.CASCADE)
	Profile_Image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	# change to password hashes later
	Password = models.CharField(max_length=256)
	Start_Date = models.DateField(auto_now_add=True)
	
	#Salt = models.CharField(max_length=100)

	def __str__(self):
		return f'Employee {self.Employee_ID}'


class Attendance(models.Model):
	Attendance_id = models.BigAutoField(primary_key=True)

	Employee_ID = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)

	DateNow = models.DateField(auto_now=True)
	Mark = models.CharField(max_length=100,null=True)
	InTime = models.CharField(max_length=256, null=True, blank=True)
	OutTime = models.CharField(max_length=256,null=True, blank=True)

	LOAN_STATUS = (
		(0, 'Pending'),
		(1, 'Present'),
		(2, 'Absent'),
	)

	status = models.IntegerField(default=0,choices=LOAN_STATUS)

	def __str__(self):
		return f'Employee_ID {self.Employee_ID}'

	class Meta:
		db_table = 'Attendance'

class WorkSchedule(models.Model):

	WorkSchedule_id = models.BigAutoField(primary_key=True)
	Employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
	Mark = models.CharField(max_length=256,null=True)

	StartDate = models.DateTimeField()
	EndDate = models.DateTimeField()


	def __str__(self):
		return f'WorkSchedule {self.Employee}'

	class Meta:
		db_table = 'WorkSchedule'

# class Admin(models.Model):
# 	Admin_id = models.BigAutoField(primary_key=True)
# 	Employee_ID = models.ForeignKey(Employee,on_delete=models.CASCADE)
# 	Full_Name = models.ForeignKey(Employee,on_delete=models.CASCADE)
# 	Phone_Number = models.ForeignKey(Employee,on_delete=models.CASCADE)
# 	Position = models.ForeignKey(Employee,on_delete=models.CASCADE)
# 	Role = models.ForeignKey(Role,on_delete=models.CASCADE)
# 	Profile_Image = models.ImageField(default='default.jpg',null=True)
# 	def __str__(self):
# 		return f'Admin {self.Employee_ID}'
