import pytest
import datetime
import calendar
from django.utils import timezone
from fakir.models import Firma, NumeracjaFaktur, LicznikFaktur, Faktura, JednostaMiary, StawkaPodatku, PozycjaFaktury, FakturaException

@pytest.mark.django_db
def test_numerowania():
    date = timezone.now()
    nr = NumeracjaFaktur.objects.create(wzorzec='TEST/{d}/{m}/{r}/{n}')
    assert nr.numer() == nr.wzorzec.format(d=date.day, m=date.month, r=date.year, n=0)

@pytest.mark.django_db
def test_tworzenia_pozycji():
    date = timezone.now()

    nr = NumeracjaFaktur.objects.create(wzorzec='FV/{d}/{m}/{r}/{n}')
    faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=date.date(), data_wystawienia=(date - datetime.timedelta(days=2)).date())

    j_m = JednostaMiary.objects.create(nazwa='ilosc')
    st_podatku = StawkaPodatku.objects.create(nazwa='VAT', stawka=0.23)

    for i in range(10):
        pozycja = PozycjaFaktury.objects.create(faktura=faktura, nazwa='Item' + str(i+1), jm=j_m, ilosc=3, cena=16.00, wartosc_netto=12.32, stawka_podatku=st_podatku)

    assert pozycja.nazwa == 'Item10'

@pytest.mark.django_db
def test_faktura_data_sprzedazy_data_wystawienia_rok_zwykly():
    nr = NumeracjaFaktur.objects.create(wzorzec='FV/{d}/{m}/{r}/{n}')
    data = datetime.date(2021, 12, 1)

    for i in range(1, 13):
        dni_w_miesiacu = calendar.monthrange(data.year, i)[1]
        data_sprzedazy = datetime.date(data.year, i, dni_w_miesiacu)
        data_wystawienia = datetime.date(data.year, i, 15) + datetime.timedelta(days=dni_w_miesiacu)

        try:
            faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=data_sprzedazy, data_wystawienia=data_wystawienia)
            faktura.save()
        except FakturaException:
            assert False, 'Data wystawienia nie moze być wystawiona dalej niz 15 dzien nastepnego miesiaca od daty sprzedazy'

    for i in range(1, 13):
        dni_w_miesiacu = calendar.monthrange(data.year, i)[1]
        data_sprzedazy = datetime.date(data.year, i, dni_w_miesiacu)
        data_wystawienia = data_sprzedazy - datetime.timedelta(days=30)

        try:
            faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=data_sprzedazy, data_wystawienia=data_wystawienia)
            faktura.save()
        except FakturaException:
            assert False, 'Data wystawienia nie moze byc wystawiona wczesniej niz 30 dni od daty sprzedazy'

    assert True

@pytest.mark.django_db
def test_faktura_data_sprzedazy_data_wystawienia_rok_przestepny():
    nr = NumeracjaFaktur.objects.create(wzorzec='FV/{d}/{m}/{r}/{n}')
    data = datetime.date(2020, 12, 1)

    for i in range(1, 13):
        dni_w_miesiacu = calendar.monthrange(data.year, i)[1]
        data_sprzedazy = datetime.date(data.year, i, dni_w_miesiacu)
        data_wystawienia = datetime.date(data.year, i, 15) + datetime.timedelta(days=dni_w_miesiacu)

        try:
            faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=data_sprzedazy, data_wystawienia=data_wystawienia)
            faktura.save()
        except FakturaException:
            assert False, 'Data wystawienia nie moze być wystawiona dalej niz 15 dzien nastepnego miesiaca od daty sprzedazy'

    for i in range(1, 13):
        dni_w_miesiacu = calendar.monthrange(data.year, i)[1]
        data_sprzedazy = datetime.date(data.year, i, dni_w_miesiacu)
        data_wystawienia = data_sprzedazy - datetime.timedelta(days=30)

        try:
            faktura = Faktura.objects.create(numeracja=nr, data_sprzedazy=data_sprzedazy, data_wystawienia=data_wystawienia)
            faktura.save()
        except FakturaException:
            assert False, 'Data wystawienia nie moze byc wystawiona wczesniej niz 30 dni od daty sprzedazy'

    assert True

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
    f = Faktura.objects.create(numeracja=numer, sprzedawca=s, nabywca=s, data_sprzedazy=timezone.now().date(), data_wystawienia=timezone.now().date())

    assert f.sprzedawca.is_sprzedawca == True, "nabywca nie może być sprzedawca"
    assert f.nabywca.is_nabywca == True, "sprzedawca nie może być nabywca"
    assert f.nabywca != f.sprzedawca, "nabywca i sprzedawca nie moga byc ta sama osoba"