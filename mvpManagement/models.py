import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.conf import settings

class User(AbstractUser):
    AGENCYMANAGER, DRIVER, CONDUCTOR, HELPER = '1', '2', '3', '4' 
    USER_CHOICES = (
        (AGENCYMANAGER, 'AgencyManager'),
        (DRIVER, 'Driver'),
        (CONDUCTOR, 'Conductor'),
        (HELPER, 'Helper'),
    )
    usertype = models.CharField(max_length=1, choices=USER_CHOICES)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)
    objects = UserManager()

class BusInfo(models.Model):    
    bnum = models.CharField(max_length=10, verbose_name="Bus Number", unique=True)
    bseater = models.IntegerField(default=0, verbose_name="Seating Capacity")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    bdate = models.DateField(auto_now_add=True, blank=True, verbose_name="Date Select")

    class Meta:
        db_table = 'bustable'

    def __str__(self):
        return self.bnum

class BusSchedule(models.Model):
    businfo = models.ForeignKey(BusInfo, null=True, blank=True, on_delete=models.SET_NULL, related_name="bus_info", verbose_name="bus information")
    broute_from = models.CharField(max_length=100,verbose_name="Bus Route From")
    broute_to = models.CharField(max_length=100,verbose_name="Bus Route To")
    btotalfare = models.IntegerField(default=0,verbose_name="Total Fare")
    businfo_driver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name = "businfo_driver", verbose_name="Bus Driver Information")
    businfo_conductor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name = "businfo_conductor", verbose_name="Bus Conductor Information")
    businfo_helper = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name = "businfo_helper", verbose_name="Bus Helper Information")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
    bus_from = models.DateField(verbose_name="Date From")
    bus_to = models.DateField(verbose_name="Date To")

# driver_obj(5).businfo_driver.all() #bus scdeuler

    class Meta:
        db_table = 'busschedule'
    
    def __str__(self):
        return self.broute_from+" to "+self.broute_to

# class BusInfoUser(models.Model):
#     businfo = models.ForeignKey(BusInfo, on_delete=models.CASCADE, related_name = "businfo_driver", verbose_name="bus information")
#     businfo_driver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_driver", verbose_name="bus driver information")
#     businfo_condutor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_condutor", verbose_name="bus conductor information")
#     businfo_helper = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_helper", verbose_name="bus helper information")
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'bususertable'
    
#     def __str__(self):
#         return self.businfo

class BusFare(models.Model):
    user_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name = "busfare_user", verbose_name="Bus Conductor Information")
    fare_bus = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, verbose_name="Select Bus")
    fare_origin = models.CharField(max_length=100, verbose_name="Origin Place")
    fare_destination = models.CharField(max_length=100, verbose_name="Destination Place")
    busfare = models.IntegerField(default=0, verbose_name="Ticket Charge")
    seatno = models.IntegerField(default=0, verbose_name="Seat Number")
    fare_date = models.DateField(verbose_name="Travel Date")

    class Meta:
        db_table = 'busfare'

    def __str__(self):
        return self.fare_origin +' to '+ self.fare_destination

class DailyExpenses(models.Model):
    dailyexpenses_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "dailyexpenses_user")
    exinfo = models.ForeignKey(BusInfo, on_delete=models.CASCADE)
    exdieselamt = models.IntegerField(default=0)
    exdieselltr = models.IntegerField(default=0)
    exfooding = models.IntegerField(default=0)
    extolltax = models.IntegerField(default=0)
    exreparing = models.IntegerField(default=0)
    exdate = models.DateField(auto_now_add=True, blank=True)
    class Meta:
        db_table = 'dailyexpenses'

    def __str__(self):
        return str(self.exdate)