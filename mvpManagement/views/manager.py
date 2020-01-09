from django.shortcuts import render, redirect, get_object_or_404
from ..forms import UserForm, BusInfoForm, BusScheduleForm
from ..models import BusInfo, BusSchedule
from django.contrib.auth.decorators import login_required
from ..decorators import manager_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()

"""Agency Manager manage action"""
"""Return User List"""
@manager_required
def user_list(request):
    user_detail = request.user.user_set.all()
    page = request.GET.get("page", 1)
    paginator_user = Paginator(user_detail, 5)
    try:
        user_detail = paginator_user.page(page)
    except PageNotAnInteger:
        user_detail = paginator_user.page(1)
    except EmptyPage:
        user_detail = paginator_user.page(paginator_user.num_pages)
    return render(
        request, "mvp_management/managers/userlist.html", {"user_detail": user_detail}
    )

"""Return Bus Information List"""
@manager_required
def bus_list(request):
    bus_detail = request.user.businfo_set.all()
    page = request.GET.get("pg", 1)
    paginator_bus = Paginator(bus_detail, 5)
    try:
        bus_detail = paginator_bus.page(page)
    except PageNotAnInteger:
        bus_detail = paginator_bus.page(1)
    except EmptyPage:
        bus_detail = paginator_bus.page(paginator_bus.num_pages)
    return render(
        request, "mvp_management/managers/buslist.html", {"bus_detail": bus_detail}
    )


"""Return User and Bus Information List"""
@manager_required
def user_bus_list(request):
    bus_detail = request.user.busschedule_set.all()
    page = request.GET.get("pg", 1)
    paginator_bus = Paginator(bus_detail, 5)
    try:
        bus_detail = paginator_bus.page(page)
    except PageNotAnInteger:
        bus_detail = paginator_bus.page(1)
    except EmptyPage:
        bus_detail = paginator_bus.page(paginator_bus.num_pages)
    return render(
        request, "mvp_management/managers/bususerlist.html", {"bus_detail": bus_detail}
    )


"""Return User Detail View"""
@manager_required
def user_details(request, id):
    if request.method == "POST":
        user_detail = get_object_or_404(User, pk=id)
        if user_detail.is_superuser:
            messages.add_message(request, messages.INFO, "No Information Avaliable")
            return render(request, "mvp_management/managers/userdetail.html")
        elif user_detail.usertype == User.UserType.AGENCYMANAGER:
            messages.add_message(request, messages.INFO, "No Information Avaliable")
            return render(request, "mvp_management/managers/userdetail.html")
        else:
            return render(
                request,
                "mvp_management/managers/userdetail.html",
                {"user_detail": user_detail},
            )
    else:
        messages.add_message(request, messages.INFO, "No Information Avaliable")
        return render(request, "mvp_management/managers/userdetail.html")


"""Create user by agency manager"""
@manager_required
def manager_create_users(request):
    if request.method == "POST":
        # if User.objects.filter(username = request.POST['username']).exists():
        #     messages.add_message(request, messages.INFO, "Username already exists")
        #     form = UserForm()
        #     return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        # elif User.objects.filter(email = request.POST['email']).exists():
        #     messages.add_message(request, messages.INFO, "Email already exists")
        #     form = UserForm()
        #     return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        # elif request.POST['usertype'] == '1':
        #     messages.add_message(request, messages.INFO, "You can not allow to create agency.")
        #     form = UserForm()
        #     return render(request, 'mvpManagement/managers/userform.html', {'form':form})
        # else:
        form = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form_instance = form.save(commit=False)
            password = User.objects.make_random_password()
            form_instance.set_password(password)
            form_instance.created_by = request.user
            form_instance.save()
            userinfo = User.objects.get(pk=form_instance.pk)
            messages.add_message(
                request,
                messages.INFO,
                "username {0} successfully created. and pasword is - {1}".format(
                    userinfo.username, password
                ),
            )
            return redirect("manager:manager_list")
        else:
            return render(
                request, "mvp_management/managers/userform.html", {"form": form}
            )
    else:
        form = UserForm()
        return render(request, "mvp_management/managers/userform.html", {"form": form})


"""Create bus information by agency manager"""
@manager_required
def manager_create_bus(request):
    if request.method == "POST":
        form = BusInfoForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.created_by = request.user
            form_instance.save()
            messages.add_message(
                request,
                messages.INFO,
                "{0} is succcessfully created by - {1}".format(
                    form_instance.bnum, str(request.user)
                ),
            )
            return redirect("manager:bus_list")
        else:
            messages.error(
                request, "Please fill correct fields."
            )
            return render(
                request, "mvp_management/managers/businfoform.html", {"form": form}
            )
    else:
        form = BusInfoForm()
        return render(
            request, "mvp_management/managers/businfoform.html", {"form": form}
        )


"""Assign Bus for User by agency manager"""
@manager_required
def manager_create_bus_user_assign(request):
    if request.method == "POST":
        form = BusScheduleForm(request.user, request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.created_by = request.user
            form_instance.save()
            messages.add_message(
                request,
                messages.INFO,
                "Record succcessfully created by - {0}".format(str(request.user)),
            )
            return redirect("manager:show_assign_bus")
        else:
            messages.add_message(request, messages.INFO, "Please use correct fields.")
            return render(
                request, "mvp_management/managers/bususerform.html", {"form": form}
            )
    else:
        form = BusScheduleForm(request.user)
        return render(
            request, "mvp_management/managers/bususerform.html", {"form": form}
        )


"""Edit User Information"""
@manager_required
def edit_user(request, id):
    if request.method == "PUT":
        user_info = get_object_or_404(User, pk=id)
        form = UserForm(data=request.PUT, instance=user_info)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                "{0} successfully updated.".format(user_info.username),
            )
            return redirect("manager:manager_list")
        return render(
            request, "mvp_management/managers/edituser.html", {"form": form, "user_info": user_info}
        )
    else:
        user_info = get_object_or_404(User, pk=id)
        form = UserForm(instance=user_info)
        return render(
            request, "mvp_management/managers/edituser.html", {"form": form, "user_info": user_info}
        )


"""Edit Bus Information"""
@manager_required
def edit_businfo(request, id):
    if request.method == "POST":
        bus_info = get_object_or_404(BusInfo, pk=id)
        form = BusInfoForm(data=request.POST, instance=bus_info)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                "{0} successfully updated.".format(bus_info.bnum),
            )
            return redirect("manager:bus_list")
        else:
            return render(
                request, "mvp_management/managers/editbusinfo.html", {"form": form}
            )
    else:
        bus_info = get_object_or_404(BusInfo, pk=id)
        form = BusInfoForm(instance=bus_info)
        return render(
            request,
            "mvp_management/managers/editbusinfo.html",
            {"form": form, "bus_info": bus_info},
        )


"""Edit Assign Bus User Information"""
@manager_required
def edit_user_bus(request, id):
    if request.method == "POST":
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusScheduleForm(request.user, data=request.POST, instance=bus_schedule)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.INFO, "{0} successfully updated.".format(bus_schedule)
            )
            return redirect("manager:show_assign_bus")
        return render(
            request, "mvp_management/managers/editbususer.html", {"form": form, "bus_info": bus_schedule}
        )
    else:
        bus_schedule = get_object_or_404(BusSchedule, pk=id)
        form = BusScheduleForm(request.user, instance=bus_schedule)
        return render(
            request,
            "mvp_management/managers/editbususer.html",
            {"form": form, "bus_info": bus_schedule},
        )


"""Delete User"""
@manager_required
def destroy_user(request, id):
    user_info = get_object_or_404(User, pk=id)
    user_info.delete()
    messages.add_message(
        request, messages.INFO, "{0} successfully deleted.".format(user_info.username)
    )
    return redirect("manager:manager_list")


"""Delete Bus Information"""
@manager_required
def destroy_bus(request, id):
    bus_info = get_object_or_404(BusInfo, pk=id)
    bus_info.delete()
    messages.add_message(
        request, messages.INFO, "{0} successfully deleted.".format(bus_info.bnum)
    )
    return redirect("manager:bus_list")


"""Delete Assign Bus User Information"""
@manager_required
def destroy_user_bus(request, id):
    bus_user_info = get_object_or_404(BusSchedule, pk=id)
    bus_user_info.delete()
    messages.add_message(
        request,
        messages.INFO,
        "{0} successfully deleted.".format(str(bus_user_info.businfo)),
    )
    return redirect("manager:show_assign_bus")
