import pytest
from fakir.models import NumeracjaFaktur, LicznikFaktur


@pytest.mark.django_db
def test_licznika():
    nr = NumeracjaFaktur.objects.create(nazwa='test', wzorzec='TEST/{d}/{m}/{r}/{n}')
    assert nr.numer() == 'TEST/13/5/2021/0'

@pytest.mark.django_db
def test_licznika_kolejny():
    nr = NumeracjaFaktur.objects.create(nazwa='test', wzorzec='FV/{d}/{m}/{r}/{n}')
    for i in range(10):
        n = nr.numer(kolejny=True)
    assert n == 'FV/13/5/2021/10'

