from django.urls import path, include
from .views import mvp_management, admin_user, manager, driver, conductor

# app_name = 'mvpManagement'
urlpatterns = [
	path('', mvp_management.home, name='home'),
	
	path('mvpmanagement/', include(([
	path('create', admin_user.admin_create_agency, name='create'),
	path('<int:id>/edit', admin_user.edit, name='edit'),
	path('<int:id>/delete', admin_user.destroy, name='delete'),
	], 'mvpManagement'), namespace='mvpmanagement')),

	path('manager/', include(([
	path('', manager.user_list, name='manager_list'),
	path('buslist', manager.bus_list, name='bus_list'),
	path('<int:id>/userdetail', manager.user_details, name='user_detail'),
    path('createuser', manager.manager_create_users, name='create_user'),
	path('<int:id>/edituser', manager.edit_user, name='edit_user'),
	path('<int:id>/deleteuser', manager.destroy_user, name='delete_user'),
    path('createbus', manager.manager_create_bus, name='create_bus'),
	path('<int:id>/editbus', manager.edit_businfo, name='edit_bus'),
	path('<int:id>/deletebus', manager.destroy_bus, name='delete_bus'),
	path('createuserbus', manager.manager_create_bus_user_assign, name='assign_bus_to_user'),
	path('showassignbus', manager.user_bus_list, name='show_assign_bus'),
	path('<int:id>/editbususer', manager.edit_user_bus, name='edit_assign_bus'),
	path('<int:id>/deletebususer', manager.destroy_user_bus, name='delete_assign_bus'),
    ], 'mvpManagement'), namespace='manager')),

	path('driver/', include(([
	path('', driver.home, name='driver_list'),
    ], 'mvpManagement'), namespace='driver')),

	path('conductor/', include(([
	path('', conductor.home_conductor, name='conductor_list'),
	path('totalbusfare', conductor.total_bus_fare, name='total_bus_fare'),
	path('<int:busid>/busfare', conductor.bus_fare, name='conductor_bus_fare'),
    ], 'mvpManagement'), namespace='conductor')),
]