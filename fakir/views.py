from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def index(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			return redirect('homepage')
	else:
		form = AuthenticationForm()
	return render(request, 'fakir/index.html', {'form': form})

