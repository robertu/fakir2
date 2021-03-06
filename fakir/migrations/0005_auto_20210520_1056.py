# Generated by Django 3.2 on 2021-05-20 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fakir', '0004_numer_on_faktura'),
    ]

    operations = [
        migrations.AddField(
            model_name='faktura',
            name='nabywca_adres',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faktura',
            name='nabywca_nazwa',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='faktura',
            name='nabywca_taxid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='faktura',
            name='sprzedawca_adres',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faktura',
            name='sprzedawca_nazwa',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='faktura',
            name='sprzedawca_taxid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
