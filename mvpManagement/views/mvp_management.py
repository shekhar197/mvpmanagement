from django.http import HttpResponse
from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from ..models import BusInfo, BusSchedule, User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.conf import settings
# User = get_user_model()
# Create your views here.

def handler404(request, *args, **argv):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

@login_required
def home(request):
    if request.user.is_superuser:
        # user_detail = User.objects.filter(parent_id = request.user)
        user_detail = request.user.user_set.all()
        page = request.GET.get('page', 1)
        paginator_user = Paginator(user_detail, 5) #26 #5 pages 
        try:
            user_detail = paginator_user.page(page)
        except PageNotAnInteger:
            user_detail = paginator_user.page(1)
        except EmptyPage:
            user_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/home.html',{'user_detail':user_detail})

    elif request.user.usertype == User.AGENCYMANAGER:
        # user_detail = User.objects.filter(parent_id = request.user)
        user_detail = request.user.user_set.all()
        page = request.GET.get('page', 1)
        paginator_user = Paginator(user_detail, 5)
        try:
            user_detail = paginator_user.page(page)
        except PageNotAnInteger:
            user_detail = paginator_user.page(1)
        except EmptyPage:
            user_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/home.html',{'user_detail':user_detail})
    
    elif request.user.usertype == User.DRIVER:
        # bus_detail = BusSchedule.objects.filter(businfo_driver_id = request.user)
        bus_detail = request.user.businfo_driver.all()
        bus_detail = bus_detail.filter(bus_from__lte=datetime.date.today(),bus_to__gte=datetime.date.today())
        page = request.GET.get('page', 1)
        paginator_user = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_user.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_user.page(1)
        except EmptyPage:
            bus_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/home.html',{'bus_detail':bus_detail})

    elif request.user.usertype == User.CONDUCTOR:
        # bus_detail = BusSchedule.objects.filter(businfo_conductor_id = request.user)
        bus_detail = request.user.businfo_conductor.all()
        bus_detail = bus_detail.filter(bus_from__lte=datetime.date.today(),bus_to__gte=datetime.date.today())
        page = request.GET.get('page', 1)
        paginator_user = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_user.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_user.page(1)
        except EmptyPage:
            bus_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/home.html',{'bus_detail':bus_detail})

    elif request.user.usertype == User.HELPER:
        # bus_detail = BusSchedule.objects.filter(businfo_helper_id = request.user)
        bus_detail = request.user.businfo_driver.all()
        bus_detail = bus_detail.filter(bus_from__lte=datetime.date.today(),bus_to__gte=datetime.date.today())
        page = request.GET.get('page', 1)
        paginator_user = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_user.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_user.page(1)
        except EmptyPage:
            bus_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/home.html',{'bus_detail':bus_detail,'today':datetime.date.today()})
    else:
        return redirect('/accounts/login')


