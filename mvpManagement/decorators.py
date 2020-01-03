from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test,login_required

manager_login_required = user_passes_test(lambda u: u.is_active and True if u.usertype == '1' else False, login_url='/accounts/login')
driver_login_required = user_passes_test(lambda u: u.is_active and True if u.usertype == '2' else False, login_url='/accounts/login')
conductor_login_required = user_passes_test(lambda u: u.is_active and True if u.usertype == '3' else False, login_url='/accounts/login')
helper_login_required = user_passes_test(lambda u: u.is_active and True if u.usertype == '4' else False, login_url='/accounts/login')
admin_login_required = user_passes_test(lambda u: u.is_active and True if u.is_superuser else False, login_url='/accounts/login')


def manager_required(view_func):
    decorated_view_func = login_required(manager_login_required(view_func), login_url='/accounts/login')
    return decorated_view_func

def driver_required(view_func):
    decorated_view_func = login_required(driver_login_required(view_func), login_url='/accounts/login')
    return decorated_view_func

def conductor_required(view_func):
    decorated_view_func = login_required(conductor_login_required(view_func), login_url='/accounts/login')
    return decorated_view_func

def helper_required(view_func):
    decorated_view_func = login_required(helper_login_required(view_func), login_url='/accounts/login')
    return decorated_view_func

def admin_required(view_func):
    decorated_view_func = login_required(admin_login_required(view_func), login_url='/accounts/login')
    return decorated_view_func


# def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and True if u.usertype == '1' else False,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# def driver_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and True if u.usertype == '2' else False,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator

# def conductor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and True if u.usertype == '3' else False,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator

# def helper_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='accounts/login'):
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and True if u.usertype == '4' else False,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator