# Generated by Django 2.2.1 on 2019-05-23 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('price', models.FloatField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangautoapi.CarBrand')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangautoapi.CarBrand')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangautoapi.CarModel')),
            ],
        ),
    ]
