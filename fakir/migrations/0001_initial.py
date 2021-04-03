from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zakup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_produktu', models.CharField(default='', max_length=100)),
                ('rodzaj_zaplaty', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Koszt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('koszt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zakup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fakir.zakup')),
            ],
        ),

    ]
