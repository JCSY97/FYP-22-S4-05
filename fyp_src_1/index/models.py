from django.db import models

# Create your models here.
# all models are to be created in index.models
def user_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.Employee_ID + instance.section
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
	Phone_Number = models.CharField(max_length=100)
	Email_Address = models.EmailField()
	Role = models.ForeignKey(Role, on_delete=models.CASCADE)
	Profile_Image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
	# change to password hashes later
	Password = models.CharField(max_length=256)
	Start_Date = models.DateField(auto_now_add=True)
	#Salt = models.CharField(max_length=100)

	def __str__(self):
		return f'Employee {self.Employee_ID}'


class Attendance(models.Model):
	Attendance_id = models.BigAutoField(primary_key=True)
	Employee_ID = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
	DateNow = models.DateField(null=True)
	Present = models.BooleanField(null=True)
	InTime = models.DateTimeField(null=True,blank=True)
	OutTime = models.DateTimeField(null=True,blank=True)
	status = models.IntegerField(default=0)
	def __str__(self):
		return f'Employee_ID {self.Employee_ID}'
	# def status_text(self):
	# 	match self.status:
	# 		case 0: 
	# 			return "Pending"
	# 		case 1:
	# 			return "present"
	# 		case other:
	# 			return 'absent'
	# class Meta:
	# 	db_table = 'Attendance'

class WorkSchedule(models.Model):
	WorkSchedule_id = models.BigAutoField(primary_key=True)
	Employee_ID = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
	DateNow = models.DateField()
	Present = models.BooleanField()
	InTime = models.DateTimeField()
	OutTime = models.DateTimeField()
	status = models.CharField(max_length=100)
	def __str__(self):
		return f'WorkSchedule {self.Employee_ID}'

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
