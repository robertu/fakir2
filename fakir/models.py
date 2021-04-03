from django.db import models

class Zakup(models.Model):
	CHOICE = [(0,'ratalny'),(1,'jednorazowy')]
	nazwa_produktu=models.CharField(max_length=100, default="")
	rodzaj_zaplaty= models.BooleanField(choices=CHOICE, default="")


class Koszt(models.Model):
	koszt = models.DecimalField(max_digits=10, decimal_places=2)
	zakup = models.ForeignKey(Zakup, on_delete=models.CASCADE)
