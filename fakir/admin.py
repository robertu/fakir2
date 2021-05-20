from django.contrib import admin
from .models import Firma, Faktura, LicznikFaktur, PozycjaFaktury, NumeracjaFaktur


class PozycjeInline(admin.TabularInline):
    model = PozycjaFaktury
    extra = 3

class FakturaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['numeracja']}),
        ('Daty', {'fields': ['data_sprzedazy', 'data_wystawienia'], 'classes': ['collapse', 'open']}),
        (None,  {'fields': ['nabywca']}),
        ('Dane nabywcy', {'fields': ['nabywca_adres', 'nabywca_taxid'], 'classes': ['collapse', 'open']}),
        (None, {'fields': ['sprzedawca']}),
        ('Dane sprzedawcy', {'fields': ['sprzedawca_adres', 'sprzedawca_taxid'], 'classes': ['collapse', 'open']}),
        (None, {'fields': ['is_oplacona', 'is_kosztowa']})
    ]
    list_display = ('numer', 'nabywca', 'sprzedawca', 'data_wystawienia')
    list_filter = ['data_wystawienia']
    inlines = [PozycjeInline]
    autocomplete_fields = ["nabywca", "sprzedawca", "numeracja"]

    def get_fields(self, request, obj=None):
        if not obj:
            return ["numeracja", "data_sprzedazy", "data_wystawienia"]
        return super().get_fields(request, obj)

class PozycjaFakturyAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'faktura', 'stawka_podatku',)

class FirmaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'taxid', )
    list_filter = ('is_nabywca', 'is_sprzedawca')
    search_fields = ("nazwa", "taxid")

class LicznikFakturAdmin(admin.ModelAdmin):
    list_display = ('numer', 'r', 'm', 'd', 'n' )
    list_filter = ('numeracja',)

class NumeracjaFakturAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'wzorzec', 'numer' )
    search_fields = ("nazwa", "wzorzec")


admin.site.register(Faktura, FakturaAdmin)
admin.site.register(Firma, FirmaAdmin)
admin.site.register(LicznikFaktur, LicznikFakturAdmin)
admin.site.register(NumeracjaFaktur, NumeracjaFakturAdmin)
admin.site.register(PozycjaFaktury, PozycjaFakturyAdmin)
