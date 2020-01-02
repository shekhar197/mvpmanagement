import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.conf import settings

class User(AbstractUser):
    USER_CHOICES = (
        ('1', 'agencymanager'),
        ('2', 'driver'),
        ('3', 'conductor'),
        ('4', 'helper'),
    )
    usertype = models.CharField(max_length=1, choices=USER_CHOICES)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)
    objects = UserManager()

# Create your models here.
class BusInfo(models.Model):    
    bnum = models.CharField(max_length=10)
    broute_from = models.CharField(max_length=100)
    broute_to = models.CharField(max_length=100)
    btrip = models.IntegerField(default=0)
    btriphrs = models.IntegerField(default=0)
    btotalfare = models.IntegerField(default=0)
    bseater = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
    bdate = models.DateField(auto_now_add=True, blank=True)
    class Meta:
        db_table = 'bustable'
    
    def __str__(self):
        return self.bnum

class BusInfoUser(models.Model):
    businfo = models.ForeignKey(BusInfo, on_delete=models.CASCADE, related_name = "businfo_driver", verbose_name="bus information")
    businfo_driver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_driver", verbose_name="bus driver information")
    businfo_condutor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_condutor", verbose_name="bus conductor information")
    businfo_helper = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "businfo_helper", verbose_name="bus helper information")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
    class Meta:
        db_table = 'bususertable'
    
    def __str__(self):
        return self.businfo

class BusFare(models.Model):
    busfare_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "busfare_user")
    bfinfo = models.ForeignKey(BusInfo, on_delete=models.CASCADE)
    bforigin = models.CharField(max_length=100)
    bfdestination = models.CharField(max_length=100)
    bffare = models.IntegerField(default=0)
    bfseatno = models.IntegerField(default=0)
    bfdate = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = 'busfare'
    
    def __str__(self):
        return self.bforigin +' to '+ self.bfdestination

class DailyExpenses(models.Model):
    dailyexpenses_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "dailyexpenses_user")
    exinfo = models.ForeignKey(BusInfo, on_delete=models.CASCADE)
    exdieselamt = models.IntegerField(default=0)
    exdieselltr = models.IntegerField(default=0)
    exfooding = models.IntegerField(default=0)
    extolltax = models.IntegerField(default=0)
    exreparing = models.IntegerField(default=0)
    exdate = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = 'dailyexpenses'
    
    def __str__(self):
        return str(self.exdate)