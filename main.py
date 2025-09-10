#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File chính để chạy ứng dụng
Đồ án Python - Mô hình MVC
"""

from app.controllers.main_controller import MainController

def main():
    """Hàm main để khởi chạy ứng dụng"""
    print("=== ĐỒ ÁN PYTHON - MÔ HÌNH MVC ===")
    
    # Khởi tạo controller chính
    controller = MainController()
    
    # Chạy ứng dụng
    controller.run()

if __name__ == "__main__":
    main()
