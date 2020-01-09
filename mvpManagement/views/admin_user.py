from django.shortcuts import render, redirect, get_object_or_404
from ..forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
from django.http import HttpResponse
from django.contrib import messages
from ..decorators import admin_required

# add comment.
"""Create user - agency manager by Admin"""
@admin_required
def admin_create_agency(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            password = User.objects.make_random_password()
            print("Username - ", form_instance.username)
            print("User password is - ", password)
            # userinfo = User.objects.get(pk=form_instance.pk)
            form_instance.set_password(password)
            form_instance.created_by = request.user
            form_instance.save()
            print(form_instance.password)
            messages.add_message(
                request,
                messages.INFO,
                "username {0} successfully created. and pasword is - {1}".format(
                    form_instance.username, password
                ),
            )
            return redirect("home")
        else:
            return render(request, "mvp_management/admin/userform.html", {"form": form})
    else:
        form = UserForm()
        return render(request, "mvp_management/admin/userform.html", {"form": form})


"""Update user - agency manager by Admin"""
@admin_required
def edit(request, id):
    if request.method == "POST":
        user_info = get_object_or_404(User, pk=id)
        form = UserForm(data=request.POST, instance=user_info)
        if form.is_valid():
            form_instance = form.save()
            messages.add_message(
                request, messages.INFO, "{0} successfully updated.".format(form_instance.username)
            )
            return redirect("home")
        return render(
            request, "mvp_management/admin/edit.html",  {"form": form, 'user_info':user_info}
        )
    else:
        user_info = get_object_or_404(User, pk=id)
        form = UserForm(instance=user_info)
        return render(
            request, "mvp_management/admin/edit.html", {"form": form, 'user_info':user_info}
        )


"""Delete user - agency manager by Admin"""
@admin_required
def destroy(request, id):
    user_info = User.objects.get(pk=id)
    user_info.delete()
    messages.add_message(
        request, messages.INFO, user_info.username + " successfully deleted."
    )
    return redirect("home")