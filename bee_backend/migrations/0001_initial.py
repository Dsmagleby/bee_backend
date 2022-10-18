# Generated by Django 4.1.2 on 2022-10-18 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=64)),
                ('number', models.IntegerField()),
                ('colour', models.CharField(max_length=16)),
                ('place', models.CharField(max_length=128)),
                ('frames', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_date', models.DateTimeField()),
                ('observation', models.TextField(blank=True, null=True)),
                ('userid', models.CharField(max_length=64)),
                ('queen', models.IntegerField()),
                ('larva', models.IntegerField()),
                ('egg', models.IntegerField()),
                ('mood', models.IntegerField()),
                ('size', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hive', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bee_backend.hive')),
            ],
        ),
    ]