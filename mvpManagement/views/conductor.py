from django.shortcuts import render,redirect,get_object_or_404
from ..forms import BusFareForm
from ..models import BusSchedule, BusFare
from django.conf import settings
from django.contrib import messages
from ..decorators import conductor_required
from django.contrib.auth.decorators import login_required

@conductor_required
def home(request,busid):
    if request.method == "GET":
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusFareForm(bus_schedule)
        return render(request,'mvpManagement/managers/editbususer.html', {'form':form,'bus_info':bus_schedule})
    elif request.method == "POST":
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusFareForm(request.user, data=request.POST, instance=bus_schedule)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO,  "successfully updated.")
            return redirect('/index/manager/showassignbus')  
        return render(request, 'mvpManagement/managers/editbususer.html', {'form':form})

    return render(request, 'mvpManagement/conductors/conductorlist.html',{'bus_detail':bus_detail})