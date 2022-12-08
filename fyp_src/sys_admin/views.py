from django.shortcuts import render

# Create your views here.
def sys_admin_home(request):
	return render(request, 'sys_admin/sys_admin_home.html')