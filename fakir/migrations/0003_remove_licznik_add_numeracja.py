# Generated by Django 3.1.7 on 2021-05-11 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fakir', '0002_remove_licznikfaktur_nazwa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faktura',
            name='licznik',
        ),
        migrations.AddField(
            model_name='faktura',
            name='numeracja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fakir.numeracjafaktur'),
        ),
    ]