from django.db import models
from django.core.validators import MinLengthValidator

class Sprzedawca(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    nazwa_firmy = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)
    NIP = models.CharField(max_length=10, validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.imie + " " + self.nazwisko

    class Meta:
        verbose_name = "Sprzedawca"
        verbose_name_plural = "Sprzedawcy"

class Kupujacy(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    nazwa_firmy = models.CharField(max_length=200, null=True)
    NIP = models.CharField(max_length=10, validators=[MinLengthValidator(10)], null=True)
    PESEL = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    adres = models.CharField(max_length=200)

    def __str__(self):
        return self.imie + " " + self.nazwisko

    class Meta:
        verbose_name = "Kupujący"
        verbose_name_plural = "Kupujący"

class LicznikFaktur(models.Model):
    nazwa = models.CharField(max_length=200, null=True)
    podatek = models.IntegerField()

    def __str__(self):
        return self.nazwa

class Faktura(models.Model):

    nazwa = models.CharField(max_length=200, null=True)
    kupujący = models.ForeignKey(Kupujacy, on_delete=models.CASCADE)
    sprzedawca = models.ForeignKey(Sprzedawca, on_delete=models.CASCADE)
    licznik = models.ForeignKey(LicznikFaktur, on_delete=models.CASCADE)
    data_wystawienia = models.DateTimeField('Data wystawienia')


    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"



class PozycjaFaktur(models.Model):
    faktura = models.ForeignKey(Faktura, on_delete=models.CASCADE)
    Nazwa_towaru_uslugi = models.CharField(max_length=200)
    J_M_CHOICES = [
        ("1", "Godzina"),
        ("2", "Sztuka"),
    ]
    J_M = models.CharField("J.M", max_length=200, choices=J_M_CHOICES, default="2")
    ilosc = models.IntegerField()
    cena = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    wartosc_netto = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    wartosc_brutto = models.DecimalField(max_digits=20, decimal_places=2, default=0)