from django.urls import path,include
from .views import mvp_management, admin_user,manager

app_name = 'mvpManagement'
urlpatterns = [
	path('', mvp_management.home, name='home'),
	path('create', admin_user.admin_create_agency, name='create'),
	path('edit/<int:id>', admin_user.edit, name='edit'),
	path('delete/<int:id>', admin_user.destroy, name='delete'),
	
	path('manager', include(([
	path('', manager.home, name='manager_list'),
    path('/createuser', manager.manager_create_users, name='create_user'),
	path('/edituser/<int:id>', manager.edit_user, name='edit_user'),
	path('/updateuser/<int:id>', manager.update_user, name='update_user'),
	path('/deleteuser/<int:id>', manager.destroy_user, name='delete_user'),
    path('/createbus', manager.manager_create_bus, name='create_bus'),
    ], 'mvpManagement'), namespace='managers')),
]