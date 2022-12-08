from django.db import models

# Create your models here.

class Employee(models.Model):
	Employee_ID = models.IntegerField()
	Full_Name = models.CharField(max_length=256)
	Phone_Number = models.CharField(max_length=256)
	Email_Address = models.EmailField()

	Profile_Image = models.ImageField(default='default.jpg')
	# change to password hashes later
	Password = models.CharField(max_length=256)
	Roles = models.IntegerField()

	def __str__(self):
		return f'Employee {self.Employee_ID}'