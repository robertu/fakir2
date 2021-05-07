from django.contrib import admin
from .models import Sprzedawca, Kupujacy, Faktura




class FakturaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'kupujący', 'sprzedawca', 'cena', 'data_wystawienia')
    list_filter = ['data_wystawienia']


class KupujacyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'imie', 'nazwisko', 'PESEL')

class SprzedawcaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'imie', 'nazwisko', 'NIP')


admin.site.register(Faktura, FakturaAdmin)
admin.site.register(Kupujacy, KupujacyAdmin)
admin.site.register(Sprzedawca, SprzedawcaAdmin)
