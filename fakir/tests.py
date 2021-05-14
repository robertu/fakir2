import pytest
import datetime
from django.utils import timezone
from fakir.models import Firma, NumeracjaFaktur, LicznikFaktur, Faktura, JednostaMiary, StawkaPodatku, PozycjaFaktury

@pytest.mark.django_db
def test_licznika():
    date = timezone.now()
    nr = NumeracjaFaktur.objects.create(wzorzec='TEST/{d}/{m}/{r}/{n}')
    assert nr.numer() == nr.wzorzec.format(d=date.day, m=date.month, r=date.year, n=0)

@pytest.mark.django_db
def test_pozycji():
    date = timezone.now()

    nr = NumeracjaFaktur.objects.create(wzorzec='FV/{d}/{m}/{r}/{n}')
    faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=date, data_wystawienia=date - datetime.timedelta(days=2))

    j_m = JednostaMiary.objects.create(nazwa='ilosc')
    st_podatku = StawkaPodatku.objects.create(nazwa='VAT', stawka=0.23)

    for i in range(10):
        pozycja = PozycjaFaktury.objects.create(faktura=faktura, nazwa='Item' + str(i+1), jm=j_m, ilosc=3, cena=16.00, wartosc_netto=12.32, stawka_podatku=st_podatku)

    assert pozycja.nazwa == 'Item10'

@pytest.mark.django_db
def test_faktury():
    date = timezone.now()
    nr = NumeracjaFaktur.objects.create(wzorzec='FV/{d}/{m}/{r}/{n}')
    faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=date - datetime.timedelta(days=2), data_wystawienia=date)
    faktura.save()
    
    faktura2 = Faktura.objects.get(pk=faktura.pk)

    assert faktura2.data_sprzedazy >= faktura2.data_wystawienia

@pytest.mark.django_db
def test_tworzenia_licznika():
    n = NumeracjaFaktur.objects.create(nazwa="testTworzenia", wzorzec="TEST/{r}/{m}/{d}/{n}")
    assert LicznikFaktur.objects.count() == 1

@pytest.mark.django_db
def test_dodawania_licznika():
    n = NumeracjaFaktur.objects.create(nazwa="TestLicznika",wzorzec="TEST/{r}/{m}/{d}/{n}")
    r = timezone.now().year
    m = timezone.now().month
    d = timezone.now().day
    for i in range(1,1000):
        assert n.numer(kolejny=True) == "TEST/{r}/{m}/{d}/{n}".format(n=i, r=r, m=m, d=d)

@pytest.mark.django_db
def test_sprzedawcy():
    numer = NumeracjaFaktur.objects.create(nazwa="TestSprzedawcy", wzorzec="TestSprzedawcy")
    s = Firma.objects.create(nazwa="1s", is_sprzedawca=True, is_nabywca=True)
    n = Firma.objects.create(nazwa="1n", is_nabywca=True)
    f = Faktura.objects.create(numeracja=numer, sprzedawca=s, nabywca=s, data_sprzedazy=datetime.date(1, 1, 1), data_wystawienia=datetime.date(1, 1, 1))

    assert f.sprzedawca.is_sprzedawca == True, "nabywca nie może być sprzedawca"
    assert f.nabywca.is_nabywca == True, "sprzedawca nie może być nabywca"
    assert f.nabywca != f.sprzedawca, "nabywca i sprzedawca nie moga byc ta sama osoba"