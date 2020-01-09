from django.shortcuts import render, redirect, get_object_or_404
from ..forms import BusFareForm
from ..models import BusSchedule, BusFare
from django.conf import settings
from django.contrib import messages
from ..decorators import conductor_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@conductor_required
def home_conductor(request):
    bus_detail = request.user.bus_fare_user.all()
    total_fare = bus_detail.aggregate(Sum('bus_fare'))
    total_fare_sum = total_fare['bus_fare__sum']
    if total_fare_sum is not None:
        total_sum = "{0} Rs".format(total_fare_sum)
    else:
        total_sum = "{0} Rs".format("0")
    page = request.GET.get("pg", 1)
    paginator_bus = Paginator(bus_detail, 5)
    try:
        bus_detail = paginator_bus.page(page)
    except PageNotAnInteger:
        bus_detail = paginator_bus.page(1)
    except EmptyPage:
        bus_detail = paginator_bus.page(paginator_bus.num_pages)
    return render(
            request, "mvp_management/conductors/conductorcreateticket.html", 
            {"bus_detail": bus_detail, "total_fare":total_sum}
        )

@conductor_required
def total_bus_fare(request):
    bus_detail = request.user.bus_fare_user.all()
    total_fare = bus_detail.aggregate(Sum('bus_fare'))
    total_fare_sum = total_fare['bus_fare__sum']
    if total_fare_sum is not None:
        total_sum = "{0} Rs".format(total_fare_sum)
    else:
        total_sum = "{0} Rs".format("0")
    page = request.GET.get("pg", 1)
    paginator_bus = Paginator(bus_detail, 5)
    try:
        bus_detail = paginator_bus.page(page)
    except PageNotAnInteger:
        bus_detail = paginator_bus.page(1)
    except EmptyPage:
        bus_detail = paginator_bus.page(paginator_bus.num_pages)
    return render(
            request, "mvp_management/conductors/conductortotalfare.html", 
            {"bus_detail": bus_detail, "total_fare":total_sum}
        )

@conductor_required
def bus_fare(request, busid):
    if request.method == "POST":
        form = BusFareForm(int(request.POST.get('bus_info')), data=request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.created_by = request.user
            form_instance.save()
            messages.add_message(request, messages.INFO, "Field created.")
            return redirect("conductor:conductor_list")
        return render(
            request, "mvp_management/conductors/busfareform.html", {"form": form}
        )
    else:
        form = BusFareForm(busid)
        return render(
            request,
            "mvp_management/conductors/busfareform.html",
            {"form": form},
        )
