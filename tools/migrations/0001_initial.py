# Generated by Django 4.0.5 on 2022-06-15 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=250, null=True)),
                ('model', models.CharField(blank=True, max_length=250, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=250, null=True)),
                ('date_of_purchase', models.DateField()),
                ('calibrated_date', models.DateField()),
                ('next_calibration_due_date', models.DateField()),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('cost_depreciation_percentage_per_year', models.IntegerField(blank=True, null=True)),
                ('initial_location', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'Tools',
            },
        ),
        migrations.CreateModel(
            name='UserTools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_date', models.DateField()),
                ('location_of_work', models.CharField(blank=True, max_length=250, null=True)),
                ('allocated', models.BooleanField(default=False)),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_tools', to='tools.tools')),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tool', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserTools',
            },
        ),
        migrations.CreateModel(
            name='UserSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.ImageField(upload_to='')),
                ('user_tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_tools', to='tools.usertools')),
            ],
            options={
                'db_table': 'UserSignature',
            },
        ),
    ]
