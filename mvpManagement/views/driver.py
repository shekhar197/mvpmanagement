from django.shortcuts import render,redirect,get_object_or_404
from ..models import BusSchedule
from django.conf import settings
from django.contrib import messages
from ..decorators import driver_required
from django.contrib.auth.decorators import login_required

@driver_required
def home(request):
    if request.user.usertype == '2':
        bus_detail = BusSchedule.objects.filter(businfo_driver_id = request.user)
        return render(request, 'mvpManagement/drivers/driverlist.html',{'bus_detail':bus_detail})
    else:
        redirect('/accounts/login/')