from django.shortcuts import render,redirect
from ..forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse

@login_required
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

@login_required
def edit(request, id):
    if request.method == "GET":  
        user_info = User.objects.get(pk=id)
        return render(request,'mvpManagement/admin/edit.html', {'user_info':user_info})
    elif request.method == "POST":
        user_info = User.objects.get(pk=id)
        form = UserForm(data=request.POST, instance=user_info)  
        if form.is_valid():  
            form.save()  
            user_detail = User.objects.all()
            messages = list()
            messages.append(user_info.username +" successfully updated.")
            return render(request, "mvpManagement/home.html", {'user_detail':user_detail, 'messages':messages} )  
        return render(request, 'mvpManagement/admin/edit.html', {'user_info':user_info})    

@login_required
def destroy(request, id):  
    user_info = User.objects.get(pk=id)
    user_info.delete()
    messages = list()
    messages.append(user_info.username +" successfully deleted.")
    user_detail = User.objects.all()
    return render(request, "mvpManagement/home.html", {'user_detail':user_detail, 'messages':messages} )  