from django.shortcuts import render,redirect
from ..forms import UserForm, BusInfoForm
from ..models import BusInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse


@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.usertype == '1':
            user_detail = User.objects.filter(parent_id = request.user)
            bus_detail = BusInfo.objects.filter(created_by_id = request.user)
            return render(request, 'mvpManagement/managers/userlist.html',{'user_detail':user_detail,'bus_detail':bus_detail})

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
            return redirect('/manager')
    else:
        if request.user.is_authenticated:
            if request.user.usertype == '1':
                form = UserForm()
                return render(request, 'mvpManagement/managers/userform.html', {'form':form})

@login_required
def manager_create_bus(request):
    if request.method == "POST":
        form = BusInfoForm(request.POST)
        if form.is_valid():
            form.save()
            bus_detail = BusInfo.objects.filter(created_by_id = request.user)
            return render(request, 'mvpManagement/managers/businfolist.html',{'bus_detail':bus_detail})
    else:
        if request.user.is_authenticated:
            if request.user.usertype == '1':
                form = BusInfoForm()
                return render(request, 'mvpManagement/managers/businfoform.html', {'form':form})

@login_required
def edit_user(request, id):  
    user_info = User.objects.get(pk=id)
    return render(request,'mvpManagement/managers/edituser.html', {'user_info':user_info})

@login_required
def update_user(request, id):  
    if request.method == "POST":
        user_info = User.objects.get(pk=id)
        form = UserForm(data=request.POST, instance=user_info)  
        if form.is_valid():  
            form.save()  
            user_detail = User.objects.filter(parent_id = request.user)
            messages = list()
            messages.append(user_info.username +" successfully updated.")
            return render(request, "mvpManagement/managers/userlist.html", {'user_detail':user_detail, 'messages':messages} )  
        return render(request, 'mvpManagement/managers/edituser.html', {'user_info':user_info})

@login_required
def destroy_user(request, id):  
    user_info = User.objects.get(pk=id)
    user_info.delete()
    messages = list()
    messages.append(user_info.username +" successfully deleted.")
    user_detail = User.objects.filter(parent_id = request.user)
    return render(request, "mvpManagement/managers/userlist.html", {'user_detail':user_detail, 'messages':messages} )  