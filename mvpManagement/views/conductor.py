from django.shortcuts import render,redirect,get_object_or_404
from ..models import BusInfo
from django.conf import settings
from django.contrib import messages
from ..decorators import conductor_required
from django.contrib.auth.decorators import login_required

@conductor_required
def home(request):
    if request.user.usertype == '3':
        bus_detail = BusInfo.objects.filter(businfo_conductor_id = request.user)
        return render(request, 'mvpManagement/conductors/conductorlist.html',{'bus_detail':bus_detail})
    else:
        redirect('/accounts/login/')