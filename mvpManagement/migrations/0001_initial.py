# Generated by Django 2.1 on 2020-01-03 08:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('usertype', models.CharField(choices=[('1', 'agencymanager'), ('2', 'driver'), ('3', 'conductor'), ('4', 'helper')], max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusFare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bforigin', models.CharField(max_length=100)),
                ('bfdestination', models.CharField(max_length=100)),
                ('bffare', models.IntegerField(default=0)),
                ('bfseatno', models.IntegerField(default=0)),
                ('bfdate', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'busfare',
            },
        ),
        migrations.CreateModel(
            name='BusInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bnum', models.CharField(max_length=10, unique=True, verbose_name='Bus Number')),
                ('bseater', models.IntegerField(default=0, verbose_name='Seating Capacity')),
                ('bdate', models.DateField(auto_now_add=True, verbose_name='Date Select')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bustable',
            },
        ),
        migrations.CreateModel(
            name='BusSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broute_from', models.CharField(max_length=100, verbose_name='Bus Route From')),
                ('broute_to', models.CharField(max_length=100, verbose_name='Bus Route To')),
                ('btotalfare', models.IntegerField(default=0, verbose_name='Total Fare')),
                ('bus_from', models.DateField(verbose_name='Date From')),
                ('bus_to', models.DateField(verbose_name='Date To')),
                ('businfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus_info', to='mvpManagement.BusInfo', verbose_name='bus information')),
                ('businfo_conductor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_conductor', to=settings.AUTH_USER_MODEL, verbose_name='Bus Conductor Information')),
                ('businfo_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_driver', to=settings.AUTH_USER_MODEL, verbose_name='Bus Driver Information')),
                ('businfo_helper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businfo_helper', to=settings.AUTH_USER_MODEL, verbose_name='Bus Helper Information')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'busschedule',
            },
        ),
        migrations.CreateModel(
            name='DailyExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exdieselamt', models.IntegerField(default=0)),
                ('exdieselltr', models.IntegerField(default=0)),
                ('exfooding', models.IntegerField(default=0)),
                ('extolltax', models.IntegerField(default=0)),
                ('exreparing', models.IntegerField(default=0)),
                ('exdate', models.DateField(auto_now_add=True)),
                ('dailyexpenses_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailyexpenses_user', to=settings.AUTH_USER_MODEL)),
                ('exinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvpManagement.BusInfo')),
            ],
            options={
                'db_table': 'dailyexpenses',
            },
        ),
        migrations.AddField(
            model_name='busfare',
            name='bfinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvpManagement.BusInfo'),
        ),
        migrations.AddField(
            model_name='busfare',
            name='busfare_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='busfare_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
