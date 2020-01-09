import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# from django.contrib.auth.models import UserManager
from django.conf import settings

'''User model inherit to create users'''
class User(AbstractUser):
    '''This model Return User Type'''
    class UserType:
        AGENCYMANAGER = 1
        DRIVER = 2
        CONDUCTOR = 3
        HELPER = 4

    USER_CHOICES = (
        (UserType.AGENCYMANAGER, _("Agency Manager")),
        (UserType.DRIVER, _("Driver")),
        (UserType.CONDUCTOR, _("Conductor")),
        (UserType.HELPER, _("Helper")),
    )
    # modify user type to int.
    # add created_at and create_by, updated_at(timestampmodel, should be abstruct, this model inherite to all the models.)
    # remove objects.
    # add comments to all model. __doc__
    # add def __str__ to each model it should return,
    # add _ for transalation to each verbose name.
    # __str__ should be return as string format, return '{0}'.format()
    # add meta to each model for oredering.
    # verbose name pulrals dalna, into the meta.
    usertype = models.IntegerField(
        default=0, choices=USER_CHOICES, verbose_name=_("User Type")
    )
    email = models.EmailField(unique=True, verbose_name=_('email address'), blank=True)
    created_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ('user__date_joined',)
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return "{0} - {1}".format(self.username, self.usertype)
    
'''This model use for Bus Information'''
class BusInfo(models.Model):
    bnum = models.CharField(max_length=10, verbose_name=_("Bus Number"), unique=True)
    bseater = models.IntegerField(default=0, verbose_name=_("Seating Capacity"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "bustable"
        ordering = ('created_at',)
        verbose_name = "Bus Info"
        verbose_name_plural = "Buses Info"

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BusInfo, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.bnum)

'''This model set bus schedule according to available users 
   driver,conductor,helper and bus information.
'''
class BusSchedule(models.Model):
    businfo = models.ForeignKey(
        BusInfo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bus_info",
        verbose_name="bus information",
    )
    broute_from = models.CharField(max_length=100, verbose_name=_("Bus Route From"))
    broute_to = models.CharField(max_length=100, verbose_name=_("Bus Route To"))
    btotalfare = models.IntegerField(default=0, verbose_name=_("Total Fare"))
    totaltrip = models.IntegerField(default=0, verbose_name=_("Total Trip"))
    businfo_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="businfo_driver",
        verbose_name=_("Bus Driver Information"),
    )
    businfo_conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="businfo_conductor",
        verbose_name=_("Bus Conductor Information"),
    )
    businfo_helper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="businfo_helper",
        verbose_name=_("Bus Helper Information"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    bus_from = models.DateField(verbose_name=_("Date From"))
    bus_to = models.DateField(verbose_name=_("Date To"))
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "busschedule"
        ordering = ('-bus_to',)
        verbose_name = "Bus Schedule"
        verbose_name_plural = "Buses Schedule"

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BusSchedule, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} to {1}".format(str(self.broute_from), str(self.broute_to))

'''This model use by conductor for generate bus fare'''
class BusFare(models.Model):
    '''Conductor have option to set trip'''
    bus_info = models.ForeignKey(
        BusSchedule,
        on_delete=models.CASCADE,
        related_name="bus_fare_info",
        verbose_name=_("Select Bus"),
    )
    fare_origin = models.CharField(max_length=100, verbose_name=_("Origin Place"))
    fare_destination = models.CharField(
        max_length=100, verbose_name=_("Destination Place")
    )
    bus_fare = models.IntegerField(default=0, verbose_name=_("Ticket Charge"))
    seat_no = models.IntegerField(default=0, verbose_name=_("Seat Number"))
    trip = models.IntegerField(
        default=0, verbose_name=_("Bus Round")
    )
    fare_date = models.DateField(verbose_name=_("Travel Date"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bus_fare_user",
        verbose_name=_("Bus Conductor Information"),
    )
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "busfare"
        ordering = ('-created_at',)
        verbose_name = "Bus Fare"
        verbose_name_plural = "Buses Fare"

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BusFare, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} to {1}".format(self.fare_origin, self.fare_destination)

'''This daily expenses calculation.'''
class DailyExpenses(models.Model):
    dex_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dailyexpenses_user",
    )
    dex_info = models.ForeignKey(
        BusInfo, on_delete=models.CASCADE, verbose_name=_("Bus Info")
    )
    dex_diesel_amt = models.IntegerField(default=0, verbose_name=_("Diesel Amount"))
    dex_diesel_ltr = models.IntegerField(default=0, verbose_name=_("Diesel Litre"))
    dex_fooding = models.IntegerField(default=0, verbose_name=_("Fooding"))
    dex_tolltax = models.IntegerField(default=0, verbose_name=_("Toll Tax"))
    dex_reparing = models.IntegerField(default=0, verbose_name=_("Reparing"))
    dex_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "dailyexpenses"
        verbose_name = "Daily Expense"
        verbose_name_plural = "Daily Expenses"

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DailyExpenses, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(str(self.dex_date))