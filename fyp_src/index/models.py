from django.db import models

# Create your models here.
# all models are to be created in index.models

class Role(models.Model):
	Role_ID = models.IntegerField()
	Role_Name = models.CharField(max_length=256)

	def __str__(self):
		return self.Role_Name

class Employee(models.Model):
	Employee_ID = models.IntegerField(primary_key=True)
	Full_Name = models.CharField(max_length=256)
	Phone_Number = models.CharField(max_length=256)
	Email_Address = models.EmailField()

	Profile_Image = models.ImageField(default='default.jpg')
	# change to password hashes later
	Password = models.CharField(max_length=256)
	Role = models.ForeignKey(Role, on_delete=models.CASCADE)

	def __str__(self):
		return f'Employee {self.Employee_ID}'

