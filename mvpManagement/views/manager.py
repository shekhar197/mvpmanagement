from django.shortcuts import render,redirect,get_object_or_404
from ..forms import UserForm, BusInfoForm, BusInfoUserForm
from ..models import BusInfo, BusInfoUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()

@login_required
def home(request):
    if request.user.usertype == '1':
        user_detail = User.objects.filter(parent_id = request.user)
        bus_detail = BusInfo.objects.filter(created_by_id = request.user)
        bus_user_detail = BusInfoUser.objects.filter(created_by_id = request.user)
        return render(request, 'mvpManagement/managers/managertablist.html',{'user_detail':user_detail,'bus_detail':bus_detail, 'bus_user_detail':bus_user_detail})

@login_required
def manager_create_users(request):
    if request.method == "POST":
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

@login_required
def manager_create_bus(request):
    if request.method == "POST":
        form = BusInfoForm(request.POST)
        if form.is_valid():
            form_instance = form.save()
            businfo = BusInfo.objects.get(pk=form_instance.pk)
            businfo.created_by = request.user
            businfo.save()
            messages.add_message(request, messages.INFO, businfo.bnum +' is succcessfully created by '+str(request.user))
            return redirect('/index/manager')
    else:
        if request.user.usertype == '1':
            form = BusInfoForm()
            return render(request, 'mvpManagement/managers/businfoform.html', {'form':form})
        else:
            return redirect('/index')

@login_required
def manager_create_bus_user_assign(request):
    if request.method == "POST":
        form = BusInfoUserForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.created_by = request.user
            form_instance.save()
            messages.add_message(request, messages.INFO, 'Record succcessfully created by '+str(request.user))
            return redirect('/index/manager')
        else:
            messages.add_message(request, messages.INFO, 'Please use correct fields.')
            form = BusInfoUserForm()
            return render(request, 'mvpManagement/managers/bususerform.html', {'form':form})
    else:
        if request.user.usertype == '1':
            form = BusInfoUserForm()
            return render(request, 'mvpManagement/managers/bususerform.html', {'form':form})
        else:
            return redirect('/index')

@login_required
def edit_businfo(request, id):  
    if request.method == "GET":
        bus_info = get_object_or_404(BusInfo, pk=id)
        return render(request,'mvpManagement/managers/editbusinfo.html', {'bus_info':bus_info})
    elif request.method == "POST":
        bus_info = get_object_or_404(BusInfo, pk=id)
        form = BusInfoForm(data=request.POST, instance=bus_info)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO, bus_info.bnum +" successfully updated.")
            return redirect('/index/manager')  
        return render(request, 'mvpManagement/managers/editbusinfo.html', {'form':form})


@login_required
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

@login_required
def destroy_user(request, id):  
    user_info = get_object_or_404(User, pk=id)
    user_info.delete()
    messages.add_message(request, messages.INFO, user_info.username +" successfully deleted.")
    return redirect('/index/manager')

@login_required
def destroy_bus(request, id):  
    bus_info = get_object_or_404(BusInfo, pk=id)
    bus_info.delete()
    messages.add_message(request, messages.INFO, bus_info.bnum +" successfully deleted.")
    return redirect('/index/manager')