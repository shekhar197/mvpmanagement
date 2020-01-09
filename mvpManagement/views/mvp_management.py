import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from ..models import BusInfo, BusSchedule, User
from django.contrib.auth.decorators import login_required

# from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# User = get_user_model()
# Create your views here.


def handler404(request, *args, **argv):
    response = render_to_response(
        "404.html", {}, context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response(
        "500.html", {}, context_instance=RequestContext(request)
    )
    response.status_code = 500
    return response


"""MVP Management home page - Manage Multiple user roles"""


@login_required
def home(request):
    current_user = request.user
    user_detail = None
    bus_detail = None
    if current_user.is_superuser:
        user_detail = current_user.user_set.all()

    elif current_user.usertype == User.UserType.AGENCYMANAGER:
        user_detail = current_user.user_set.all()

    elif current_user.usertype == User.UserType.DRIVER:
        bus_detail = current_user.businfo_driver.all()
        bus_detail = bus_detail.filter(
            bus_from__lte=datetime.date.today(), bus_to__gte=datetime.date.today()
        )

    elif current_user.usertype == User.UserType.CONDUCTOR:
        bus_detail = current_user.businfo_conductor.all()
        bus_detail = bus_detail.filter(
            bus_from__lte=datetime.date.today(), bus_to__gte=datetime.date.today()
        )

    elif current_user.usertype == User.UserType.HELPER:
        bus_detail = current_user.businfo_driver.all()
        bus_detail = bus_detail.filter(
            bus_from__lte=datetime.date.today(), bus_to__gte=datetime.date.today()
        )

    if user_detail is not None:
        page = request.GET.get("page", 1)
        paginator_user = Paginator(user_detail, 5)
        try:
            user_detail = paginator_user.page(page)
        except PageNotAnInteger:
            user_detail = paginator_user.page(1)
        except EmptyPage:
            user_detail = paginator_user.page(paginator_user.num_pages)
        context = {'user_detail': user_detail}
        return render(request, "mvp_management/home.html", context)

    elif bus_detail is not None:
        page = request.GET.get("page", 1)
        paginator_user = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_user.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_user.page(1)
        except EmptyPage:
            bus_detail = paginator_user.page(paginator_user.num_pages)
        context = {"bus_detail": bus_detail, "today": datetime.date.today()}
        return render(request, "mvp_management/home.html", context)

    else:
        messages.add_message(request, messages.INFO, "No Information Avaliable.")
        return render(request, "mvp_management/home.html")