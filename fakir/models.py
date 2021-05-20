from django.db import models
import datetime
import calendar
from django.core.validators import MinLengthValidator
from django.db.models.fields import DecimalField
from decimal import Decimal
from django.utils import timezone
from django.db.models.signals import post_save, pre_save


class Firma(models.Model):
    nazwa = models.CharField(max_length=200)
    adres = models.TextField()
    taxid = models.CharField(max_length=20, null=True, blank=True)
    is_sprzedawca = models.BooleanField(default=False)
    is_nabywca = models.BooleanField(default=False)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Sprzedawcy"


class NumeracjaFaktur(models.Model):
    nazwa = models.CharField(max_length=200, unique=True)
    # uzywaj_r = models.BooleanField(default=False)
    # uzywaj_m = models.BooleanField(default=False)
    # uzywaj_d = models.BooleanField(default=False)
    wzorzec = models.CharField(max_length=200, help_text="We wzorcu używaj znaczników: {r},{m},{d},{n} do wartości rok, miesiąc, dzień, numer")

    def __str__(self):
        return f"{self.nazwa} {self.wzorzec}"

    def get_licznik_from_date(self, date):

        r = date.year if "{r}" in self.wzorzec else 0
        m = date.month if "{m}" in self.wzorzec else 0
        d = date.day if "{d}" in self.wzorzec else 0

        l, created = LicznikFaktur.objects.get_or_create(numeracja=self, r=r, m=m, d=d)
        return l

    def get_current_licznik(self):
        return self.get_licznik_from_date(timezone.now())

    def numer(self, licznik=None, kolejny=False):
        if licznik is None:
            licznik = self.get_current_licznik()
        if kolejny:
            licznik.n += 1
            licznik.save()
        return self.wzorzec.format(n=licznik.n, r=licznik.r, m=licznik.m, d=licznik.d)


class LicznikFaktur(models.Model):
    numeracja = models.ForeignKey(NumeracjaFaktur, on_delete=models.CASCADE, related_name="licznik_set")
    r = models.PositiveBigIntegerField(default=0)
    m = models.PositiveBigIntegerField(default=0)
    d = models.PositiveBigIntegerField(default=0)
    n = models.PositiveBigIntegerField(default=0)

    @property
    def numer(self):
        return self.numeracja.numer(licznik=self)

    def __str__(self):
        return self.numer


class Faktura(models.Model):

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"

    numer = models.CharField(max_length=200, null=True, blank=True,)

    nabywca = models.ForeignKey(Firma, on_delete=models.SET_NULL, null=True, blank=True, related_name="nabywcy_set")
    nabywca_adres = models.TextField(null=True, blank=True)
    nabywca_taxid = models.CharField(max_length=20, null=True, blank=True)

    sprzedawca = models.ForeignKey(Firma, on_delete=models.SET_NULL, null=True, blank=True, related_name="sprzedawcy_set")
    sprzedawca_adres = models.TextField(null=True, blank=True)
    sprzedawca_taxid = models.CharField(max_length=20, null=True, blank=True)

    numeracja = models.ForeignKey(NumeracjaFaktur, on_delete=models.SET_NULL, null=True, blank=True)
    data_sprzedazy = models.DateField('Data sprzedaży')
    data_wystawienia = models.DateField('Data wystawienia')
    is_oplacona = models.BooleanField(default=False)
    is_kosztowa = models.BooleanField(default=False)

    def __str__(self):
        return self.numer


class KontoBankowe(models.Model):
    numer = models.CharField(max_length=26)


class JednostaMiary(models.Model):
    nazwa = models.CharField(max_length=20)


class StawkaPodatku(models.Model):
    nazwa = models.CharField(max_length=20, unique=True)
    stawka = models.DecimalField(max_digits=5, decimal_places=2, default=0, unique=True)


class PozycjaFaktury(models.Model):
    faktura = models.ForeignKey(Faktura, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200)
    jm = models.ForeignKey(JednostaMiary, on_delete=models.SET_NULL, null=True, blank=True)
    ilosc = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('1.0'))
    cena = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    wartosc_netto = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    stawka_podatku = models.ForeignKey(StawkaPodatku, null=True, blank=True, on_delete=models.SET_NULL)


class FakturaException(Exception):
    pass


def wyznacz_numer(sender, instance, **_kwargs):

    instance.numer = instance.numeracja.numer(kolejny=True) if not instance.numer else instance.numeracja.numer()


def sprawdz_date_wystawienia_sprzedazy(sender, instance, **_kwargs):
    sprzedaz = instance.data_sprzedazy
    wystawienie = instance.data_wystawienia

    dni_w_miesiacu = calendar.monthrange(sprzedaz.year, sprzedaz.month)[1]
    data_15_dni_nast_miesiaca = datetime.date(sprzedaz.year, sprzedaz.month, 15) + datetime.timedelta(days=dni_w_miesiacu)

    if sprzedaz - datetime.timedelta(days=30) > wystawienie:
        raise FakturaException('Data wystawienia nie moze byc wystawiona wczesniej niz 30 dni od daty sprzedazy')
    elif wystawienie > data_15_dni_nast_miesiaca:
        raise FakturaException('Data wystawienia nie moze być wystawiona dalej niz 15 dzien nastepnego miesiaca od daty sprzedazy')


def kopiuj_dane_z_firmy(sender, instance, **_kwargs):
    nabywca = instance.nabywca
    sprzedawca = instance.sprzedawca

    if(nabywca and sprzedawca):
        instance.nabywca_adres = nabywca.adres
        instance.nabywca_taxid = nabywca.taxid

        instance.sprzedawca_adres = sprzedawca.adres
        instance.sprzedawca_taxid = sprzedawca.taxid


pre_save.connect(wyznacz_numer, sender=Faktura)
pre_save.connect(sprawdz_date_wystawienia_sprzedazy, sender=Faktura)
pre_save.connect(kopiuj_dane_z_firmy, sender=Faktura)
