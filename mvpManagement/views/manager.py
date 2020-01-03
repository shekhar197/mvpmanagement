from django.shortcuts import render,redirect,get_object_or_404
from ..forms import UserForm, BusInfoForm, BusScheduleForm
from ..models import BusInfo, BusSchedule
from django.contrib.auth.decorators import login_required
from ..decorators import manager_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = get_user_model()


@manager_required
def userlist(request):
    if request.user.usertype == '1':
        user_detail = User.objects.filter(parent_id = request.user)
        page = request.GET.get('page', 1)
        paginator_user = Paginator(user_detail, 5)
        try:
            user_detail = paginator_user.page(page)
        except PageNotAnInteger:
            user_detail = paginator_user.page(1)
        except EmptyPage:
            user_detail = paginator_user.page(paginator_user.num_pages)
        return render(request, 'mvpManagement/managers/userlist.html',{'user_detail':user_detail})
    else:
        redirect('/index')

@manager_required
def buslist(request):
    if request.user.usertype == '1':
        bus_detail = BusInfo.objects.filter(created_by_id = request.user)
        page = request.GET.get('pg', 1)
        paginator_bus = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_bus.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_bus.page(1)
        except EmptyPage:
            bus_detail = paginator_bus.page(paginator_bus.num_pages)
        return render(request, 'mvpManagement/managers/buslist.html',{'bus_detail':bus_detail})
    else:
        redirect('/index')

@manager_required
def userbuslist(request):
    if request.user.usertype == '1':
        bus_detail = BusSchedule.objects.filter(created_by_id = request.user)
        for bus in bus_detail:
            print(bus.__dict__)
        page = request.GET.get('pg', 1)
        paginator_bus = Paginator(bus_detail, 5)
        try:
            bus_detail = paginator_bus.page(page)
        except PageNotAnInteger:
            bus_detail = paginator_bus.page(1)
        except EmptyPage:
            bus_detail = paginator_bus.page(paginator_bus.num_pages)
        return render(request, 'mvpManagement/managers/bususerlist.html',{'bus_detail':bus_detail})
    else:
        redirect('/index')

@manager_required
def userdetails(request, id):
    if request.user.usertype == '1':
        if request.method == "POST":
            user_detail = get_object_or_404(User, pk=id)
            if user_detail.is_superuser:
                messages.add_message(request, messages.INFO, "No Information Avaliable")
                return render(request, 'mvpManagement/managers/userdetail.html')
            elif user_detail.usertype == '1':
                messages.add_message(request, messages.INFO, "No Information Avaliable")
                return render(request, 'mvpManagement/managers/userdetail.html')
            else:
                return render(request, 'mvpManagement/managers/userdetail.html',{'user_detail':user_detail})
        else:
            messages.add_message(request, messages.INFO, "No Information Avaliable")
            return render(request, 'mvpManagement/managers/userdetail.html')

@manager_required
def manager_create_users(request):
    if request.method == "POST":
        if User.objects.filter(username = request.POST['username']).exists():
            messages.add_message(request, messages.INFO, "Username already exists")
            form = UserForm()
            return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        elif User.objects.filter(email = request.POST['email']).exists():
            messages.add_message(request, messages.INFO, "Email already exists")
            form = UserForm()
            return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        elif request.POST['usertype'] == '1':
            messages.add_message(request, messages.INFO, "You can not allow to create agency.")
            form = UserForm()
            return render(request, 'mvpManagement/managers/userform.html', {'form':form})    
        else:
            form = UserForm(request.POST)
            if form.is_valid():
                form_instance = form.save()
                password = User.objects.make_random_password()
                print("Username - ",form_instance.username)
                print("User password is - ",password)
                userinfo = User.objects.get(pk=form_instance.pk)
                userinfo.set_password(password)
                userinfo.parent = request.user
                userinfo.save()
                messages.add_message(request, messages.INFO, "username '"+ form_instance.username +"' successfully created. and pasword is - "+password)
                return redirect('/index/manager')
    else:
        if request.user.usertype == '1':
            form = UserForm()
            return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        else:
            return redirect('/index')

@manager_required
def manager_create_bus(request):
    if request.method == "POST":
        if BusInfo.objects.filter(bnum = request.POST['bnum']).exists():
            messages.add_message(request, messages.INFO, "Bus Number already exists")
            form = BusInfoForm()
            return render(request, 'mvpManagement/managers/businfoform.html', {'form':form})
        else:
            form = BusInfoForm(request.POST)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.created_by = request.user
                form_instance.save()
                messages.add_message(request, messages.INFO, form_instance.bnum +' is succcessfully created by '+str(request.user))
                return redirect('/index/manager/buslist')
            else:
                messages.add_message(request, messages.INFO, "Please Use Correct Fields.")
                form = BusInfoForm()
                return render(request, 'mvpManagement/managers/businfoform.html', {'form':form})
    else:
        if request.user.usertype == '1':
            form = BusInfoForm()
            return render(request, 'mvpManagement/managers/businfoform.html', {'form':form})
        else:
            return redirect('/index')

@manager_required
def manager_create_bus_user_assign(request):
    if request.method == "POST":
        form = BusScheduleForm(request.user,request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.created_by = request.user
            form_instance.save()
            messages.add_message(request, messages.INFO, 'Record succcessfully created by '+str(request.user))
            return redirect('/index/manager/showassignbus')
        else:
            messages.add_message(request, messages.INFO, 'Please use correct fields.')
            form = BusScheduleForm(request.user)
            return render(request, 'mvpManagement/managers/bususerform.html', {'form':form})
    else:
        if request.user.usertype == '1':
            form = BusScheduleForm(request.user)
            return render(request, 'mvpManagement/managers/bususerform.html', {'form':form})
        else:
            return redirect('/index')

@manager_required
def edit_user(request, id):  
    if request.method == "GET":
        user_info = get_object_or_404(User, pk=id)
        return render(request,'mvpManagement/managers/edituser.html', {'user_info':user_info})
    elif request.method == "POST":
        user_info = get_object_or_404(User, pk=id)
        form = UserForm(data=request.POST, instance=user_info)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO, user_info.username +" successfully updated.")
            return redirect('/index/manager')  
        return render(request, 'mvpManagement/managers/edituser.html', {'user_info':user_info})

@manager_required
def edit_businfo(request, id):  
    if request.method == "GET":
        bus_info = get_object_or_404(BusInfo, pk=id)
        form = BusInfoForm(instance=bus_info)
        return render(request,'mvpManagement/managers/editbusinfo.html', {'form':form,'bus_info':bus_info})
    elif request.method == "POST":
        bus_info = get_object_or_404(BusInfo, pk=id)
        form = BusInfoForm(data=request.POST, instance=bus_info)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO, bus_info.bnum +" successfully updated.")
            return redirect('/index/manager')  
        return render(request, 'mvpManagement/managers/editbusinfo.html', {'form':form})

@manager_required
def edit_user_bus(request, id):  
    if request.method == "GET":
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusScheduleForm(request.user, instance=bus_schedule)
        return render(request,'mvpManagement/managers/editbususer.html', {'form':form,'bus_info':bus_schedule})
    elif request.method == "POST":
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusScheduleForm(request.user, data=request.POST, instance=bus_schedule)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO,  "successfully updated.")
            return redirect('/index/manager/showassignbus')  
        return render(request, 'mvpManagement/managers/editbususer.html', {'form':form})

@manager_required
def destroy_user(request, id):  
    user_info = get_object_or_404(User, pk=id)
    user_info.delete()
    messages.add_message(request, messages.INFO, user_info.username +" successfully deleted.")
    return redirect('/index/manager')

@manager_required
def destroy_bus(request, id):  
    bus_info = get_object_or_404(BusInfo, pk=id)
    bus_info.delete()
    messages.add_message(request, messages.INFO, bus_info.bnum +" successfully deleted.")
    return redirect('/index/manager')

@manager_required
def destroy_user_bus(request, id):  
    bus_user_info = get_object_or_404(BusSchedule, pk=id)
    bus_user_info.delete()
    messages.add_message(request, messages.INFO, bus_user_info.bus_info +" successfully deleted.")
    return redirect('/index/manager')