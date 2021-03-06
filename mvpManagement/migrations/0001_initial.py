# Generated by Django 2.1 on 2020-01-09 08:28

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0010_auto_20200109_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('usertype', models.IntegerField(choices=[(1, 'Agency Manager'), (2, 'Driver'), (3, 'Conductor'), (4, 'Helper')], default=0, verbose_name='User Type')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('user__date_joined',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusFare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fare_origin', models.CharField(max_length=100, verbose_name='Origin Place')),
                ('fare_destination', models.CharField(max_length=100, verbose_name='Destination Place')),
                ('bus_fare', models.IntegerField(default=0, verbose_name='Ticket Charge')),
                ('seat_no', models.IntegerField(default=0, verbose_name='Seat Number')),
                ('trip', models.IntegerField(default=0, verbose_name='Bus Round')),
                ('fare_date', models.DateField(verbose_name='Travel Date')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Bus Fare',
                'verbose_name_plural': 'Buses Fare',
                'db_table': 'busfare',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='BusInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bnum', models.CharField(max_length=10, unique=True, verbose_name='Bus Number')),
                ('bseater', models.IntegerField(default=0, verbose_name='Seating Capacity')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bus Info',
                'verbose_name_plural': 'Buses Info',
                'db_table': 'bustable',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='BusSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broute_from', models.CharField(max_length=100, verbose_name='Bus Route From')),
                ('broute_to', models.CharField(max_length=100, verbose_name='Bus Route To')),
                ('btotalfare', models.IntegerField(default=0, verbose_name='Total Fare')),
                ('totaltrip', models.IntegerField(default=0, verbose_name='Total Trip')),
                ('bus_from', models.DateField(verbose_name='Date From')),
                ('bus_to', models.DateField(verbose_name='Date To')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('businfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus_info', to='mvpManagement.BusInfo', verbose_name='bus information')),
                ('businfo_conductor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_conductor', to=settings.AUTH_USER_MODEL, verbose_name='Bus Conductor Information')),
                ('businfo_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_driver', to=settings.AUTH_USER_MODEL, verbose_name='Bus Driver Information')),
                ('businfo_helper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_helper', to=settings.AUTH_USER_MODEL, verbose_name='Bus Helper Information')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bus Schedule',
                'verbose_name_plural': 'Buses Schedule',
                'db_table': 'busschedule',
                'ordering': ('-bus_to',),
            },
        ),
        migrations.CreateModel(
            name='DailyExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dex_diesel_amt', models.IntegerField(default=0, verbose_name='Diesel Amount')),
                ('dex_diesel_ltr', models.IntegerField(default=0, verbose_name='Diesel Litre')),
                ('dex_fooding', models.IntegerField(default=0, verbose_name='Fooding')),
                ('dex_tolltax', models.IntegerField(default=0, verbose_name='Toll Tax')),
                ('dex_reparing', models.IntegerField(default=0, verbose_name='Reparing')),
                ('dex_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('dex_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvpManagement.BusInfo', verbose_name='Bus Info')),
                ('dex_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailyexpenses_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Daily Expense',
                'verbose_name_plural': 'Daily Expenses',
                'db_table': 'dailyexpenses',
            },
        ),
        migrations.AddField(
            model_name='busfare',
            name='bus_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_fare_info', to='mvpManagement.BusSchedule', verbose_name='Select Bus'),
        ),
        migrations.AddField(
            model_name='busfare',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus_fare_user', to=settings.AUTH_USER_MODEL, verbose_name='Bus Conductor Information'),
        ),
    ]
