# Generated by Django 4.2.1 on 2023-05-10 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('LifeRemaining', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Toner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Colour', models.CharField(max_length=200)),
                ('Percent', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tray',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Status', models.CharField(max_length=200)),
                ('Capacity', models.CharField(max_length=200)),
                ('PageSize', models.CharField(max_length=200)),
                ('PageType', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Model', models.CharField(max_length=200)),
                ('Address', models.CharField(max_length=200)),
                ('Location', models.CharField(max_length=200)),
                ('MaintenanceKit', models.CharField(max_length=200)),
                ('PCKit', models.CharField(max_length=200)),
                ('Buffer', models.CharField(max_length=200)),
                ('HtmlTopBar', models.CharField(max_length=200)),
                ('HtmlStatus', models.CharField(max_length=200)),
                ('Status', models.CharField(max_length=200)),
                ('Kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printers.kit')),
                ('Toner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printers.toner')),
                ('Tray', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printers.tray')),
            ],
        ),
    ]
