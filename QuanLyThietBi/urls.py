"""
URL configuration for QuanLyThietBi project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Hello World API
    path('api/hello/', views.hello_world, name='hello_world'),
    
    # PhongBan APIs
    path('api/phongban/', views.get_phongban_list, name='phongban_list'),
    path('api/phongban/create/', views.create_phongban, name='create_phongban'),
    path('api/phongban/<str:ma_phong_ban>/', views.get_phongban_by_id, name='phongban_detail'),
    path('api/phongban/<str:ma_phong_ban>/update/', views.update_phongban, name='update_phongban'),
    path('api/phongban/<str:ma_phong_ban>/delete/', views.delete_phongban, name='delete_phongban'),
    path('api/phongban/search/', views.search_phongban, name='search_phongban'),
    
    # NhanVien APIs
    path('api/nhanvien/', views.get_nhanvien_list, name='nhanvien_list'),
    path('api/nhanvien/create/', views.create_nhanvien, name='create_nhanvien'),
    path('api/nhanvien/<str:ma_nhan_vien>/', views.get_nhanvien_by_id, name='nhanvien_detail'),
    path('api/nhanvien/<str:ma_nhan_vien>/update/', views.update_nhanvien, name='update_nhanvien'),
    path('api/nhanvien/<str:ma_nhan_vien>/delete/', views.delete_nhanvien, name='delete_nhanvien'),
    path('api/nhanvien/search/', views.search_nhanvien, name='search_nhanvien'),
    path('api/nhanvien/phongban/<str:ma_phong_ban>/', views.get_nhanvien_by_phongban, name='nhanvien_by_phongban'),
    path('api/nhanvien/auth/', views.authenticate_nhanvien, name='authenticate_nhanvien'),
]
