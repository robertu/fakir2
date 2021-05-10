from django.contrib import admin
from .models import Sprzedawca, Kupujacy, Faktura, LicznikFaktur, PozycjaFaktur


class PozycjeInline(admin.TabularInline):
    model = PozycjaFaktur
    extra = 3

class FakturaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kupujący', 'sprzedawca', 'data_wystawienia')
    list_filter = ['data_wystawienia']
    inlines = [PozycjeInline]

class KupujacyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'imie', 'nazwisko', 'PESEL')

class SprzedawcaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'imie', 'nazwisko', 'NIP')


admin.site.register(Faktura, FakturaAdmin)
admin.site.register(Kupujacy, KupujacyAdmin)
admin.site.register(Sprzedawca, SprzedawcaAdmin)
admin.site.register(LicznikFaktur)
admin.site.register(PozycjaFaktur)
