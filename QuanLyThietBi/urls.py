from django.urls import path
from .controllers import views

urlpatterns = [
    # Chức năng chung cho cả Admin và Nhân viên
    path('devices/', views.list_all_devices, name='list-all-devices'),

    # Chức năng của ADMIN
    path('admin/devices/create/', views.create_device, name='admin-create-device'),
    path('admin/devices/update/<str:maTB>/', views.update_device, name='admin-update-device'),
    path('admin/devices/in-use/', views.list_devices_in_use, name='admin-list-devices-in-use'),
    path('admin/requests/', views.list_all_requests, name='admin-list-all-requests'),
    path('admin/requests/approve/<str:maYC>/', views.approve_request, name='admin-approve-request'),
    path('admin/requests/reject/<str:maYC>/', views.reject_request, name='admin-reject-request'),

    # Chức năng của Nhân viên
    path('staff/requests/create/', views.create_request, name='staff-create-request'),
    path('staff/requests/', views.list_my_requests, name='staff-list-requests'),
]