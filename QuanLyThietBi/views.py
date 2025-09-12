# QuanLyThietBi/views.py
from .Views.hello import hello_world
from .Views.phongban import get_phongban_list, create_phongban, get_phongban_by_id, update_phongban, delete_phongban, search_phongban
from .Views.nhanvien import (
    get_nhanvien_list, 
    get_nhanvien_by_id, 
    create_nhanvien, 
    update_nhanvien, 
    delete_nhanvien, 
    search_nhanvien, 
    get_nhanvien_by_phongban,
    authenticate_nhanvien
)
