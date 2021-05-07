from django.db import models

class Sprzedawca(models.Model):
    NIP = models.CharField(max_length=13, null=True)
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)

    def __str__(self):
        return self.imie + " " + self.nazwisko

    class Meta:
        verbose_name = "Sprzedawca"
        verbose_name_plural = "Sprzedawcy"

class Kupujacy(models.Model):
    PESEL = models.DecimalField(max_digits=11, decimal_places=0, default=10000000000)
    imie = models.CharField(max_length=200)
    nazwisko = models.CharField(max_length=200)
    adres = models.CharField(max_length=200)

    def __str__(self):
        return self.imie + " " + self.nazwisko

    class Meta:
        verbose_name = "Kupujący"
        verbose_name_plural = "Kupujący"

class Faktura(models.Model):

    kupujący = models.ForeignKey(Kupujacy, on_delete=models.CASCADE, null=True)
    sprzedawca = models.ForeignKey(Sprzedawca, on_delete=models.CASCADE, null=True)
    data_wystawienia = models.DateTimeField('Data wystawienia')
    cena = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # def __str__(self):
    #     return self.pk

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Faktury"