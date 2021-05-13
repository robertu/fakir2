import pytest
import django
django.setup()
from .models import NumeracjaFaktur, LicznikFaktur

# Create your tests here.
def test_licznika():
    nr = NumeracjaFaktur.objects.create(nazwa='test', wzorzec='{d}/{m}/{r}/{n}')
    assert nr.numer() == '12/5/2021/0'
