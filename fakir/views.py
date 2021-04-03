from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.

def index(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/manage/')
	else:
		form = AuthenticationForm()
	return render(request, 'fakir/index.html', {'form': form})

def manage(request):
    return render(request, 'fakir/manage.html')