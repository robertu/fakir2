from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Faktura, PozycjaFaktury
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

@staff_member_required
def FakturaView(request, pk):
	faktura = get_object_or_404(Faktura, pk=pk)
	pozycje = faktura.pozycjafaktury_set

	return render(request, 'fakir/faktura_view.html', context={'faktura': faktura, 'pozycje': pozycje})