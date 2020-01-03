from django.urls import path,include
from .views import mvp_management, admin_user, manager, driver, conductor

app_name = 'mvpManagement'
urlpatterns = [
	path('', mvp_management.home, name='home'),
	path('create', admin_user.admin_create_agency, name='create'),
	path('edit/<int:id>', admin_user.edit, name='edit'),
	path('delete/<int:id>', admin_user.destroy, name='delete'),
	
	path('manager', include(([
	path('', manager.userlist, name='manager_list'),
	path('/buslist', manager.buslist, name='manager_list'),
	path('/userdetail/<int:id>', manager.userdetails, name='user_detail'),
    path('/createuser', manager.manager_create_users, name='create_user'),
	path('/edituser/<int:id>', manager.edit_user, name='edit_user'),
	path('/deleteuser/<int:id>', manager.destroy_user, name='delete_user'),
    path('/createbus', manager.manager_create_bus, name='create_bus'),
	path('/editbus/<int:id>', manager.edit_businfo, name='edit_bus'),
	path('/deletebus/<int:id>', manager.destroy_bus, name='delete_bus'),
	path('/createuserbus', manager.manager_create_bus_user_assign, name='assign_bus_to_user'),
	path('/showassignbus', manager.userbuslist, name='show_assign_bus'),
	path('/editbususer/<int:id>', manager.edit_user_bus, name='edit_assign_bus'),
	path('/deletebususer/<int:id>', manager.destroy_user_bus, name='delete_assign_bus'),
    ], 'mvpManagement'), namespace='managers')),

	path('driver', include(([
	path('', driver.home, name='driver_list'),
    ], 'mvpManagement'), namespace='drivers')),

	path('conductor', include(([
	path('', conductor.home, name='driver_list'),
    ], 'mvpManagement'), namespace='conductors')),
]