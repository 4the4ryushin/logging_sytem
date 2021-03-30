from django.shortcuts import render , redirect
from django.contrib.auth import login#added
from django.contrib.auth.forms import UserCreationForm #added


# Create your views here.
def register(request):
	"""register a new user"""
	if request.method !='POST':
		#display blank registration form.
		form=UserCreationForm()

	else:
		#process data.
		form=UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user=form.save()
			#Log the user in and then redirect to home page.
			login(request,new_user)
			return redirect('learning_logs:index')

	#Display a blankor invalid form.
	context= {'form':form}
	return render(request,'registration/register.html',context)
