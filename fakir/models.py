from django.db import models

class Sprzedawca(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)

class Kupujacy(models.Model):
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)
