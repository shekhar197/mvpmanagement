from django.shortcuts import render,redirect
from ..forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse
from django.contrib import messages
from ..decorators import admin_required

@admin_required
def admin_create_agency(request):
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
            print(userinfo.password)
            return render(request, 'mvpManagement/pageview.html',{'userinfo':userinfo,'password':password})
    else:
        if request.user.is_superuser:
            form = UserForm()
            return render(request, 'mvpManagement/admin/userform.html', {'form':form})

@admin_required
def edit(request, id):
    if request.method == "GET":  
        user_info = User.objects.get(pk=id)
        return render(request,'mvpManagement/admin/edit.html', {'user_info':user_info})
    elif request.method == "POST":
        user_info = User.objects.get(pk=id)
        form = UserForm(data=request.POST, instance=user_info)  
        if form.is_valid():  
            form.save()  
            messages.add_message(request, messages.INFO, user_info.username +" successfully updated.")
            return redirect('/index')
        return render(request, 'mvpManagement/admin/edit.html', {'user_info':user_info})    

@admin_required
def destroy(request, id):  
    user_info = User.objects.get(pk=id)
    user_info.delete()
    messages.add_message(request, messages.INFO, user_info.username +" successfully deleted.")
    return redirect('/index')