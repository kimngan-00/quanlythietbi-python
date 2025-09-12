from django.db import connection
from django.http import JsonResponse
import json
import hashlib
from ..utils import JWTUtils

class NhanVienController:
    """
    Controller xử lý các thao tác với nhân viên
    """
    
    @staticmethod
    def get_nhanvien_list():
        """
        Lấy danh sách tất cả nhân viên
        """
        try:
            with connection.cursor() as cursor:
                # SQL query để lấy danh sách nhân viên
                cursor.execute("""
                    SELECT nv.maNhanVien, nv.tenNhanVien, nv.email, nv.soDienThoai, 
                           nv.role, nv.maPhongBan, pb.tenPhongBan, nv.ngayTao
                    FROM NhanVien nv
                    LEFT JOIN PhongBan pb ON nv.maPhongBan = pb.maPhongBan
                    ORDER BY nv.maNhanVien
                """)
                
                # Lấy tất cả kết quả
                results = cursor.fetchall()
                
                # Chuyển đổi thành danh sách dictionary
                nhanvien_list = []
                for row in results:
                    nhanvien_list.append({
                        'maNhanVien': row[0],
                        'tenNhanVien': row[1],
                        'email': row[2],
                        'soDienThoai': row[3] if row[3] else '',
                        'role': row[4],
                        'maPhongBan': row[5],
                        'tenPhongBan': row[6] if row[6] else '',
                        'ngayTao': row[7].strftime('%Y-%m-%d %H:%M:%S') if row[7] else ''
                    })
                
                return {
                    'success': True,
                    'data': nhanvien_list,
                    'message': 'Lấy danh sách nhân viên thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi lấy danh sách nhân viên: {str(e)}'
            }
    
    @staticmethod
    def get_nhanvien_by_id(ma_nhan_vien):
        """
        Lấy thông tin nhân viên theo mã
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nv.maNhanVien, nv.tenNhanVien, nv.email, nv.soDienThoai, 
                           nv.role, nv.maPhongBan, pb.tenPhongBan, nv.ngayTao
                    FROM NhanVien nv
                    LEFT JOIN PhongBan pb ON nv.maPhongBan = pb.maPhongBan
                    WHERE nv.maNhanVien = %s
                """, [ma_nhan_vien])
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'success': True,
                        'data': {
                            'maNhanVien': result[0],
                            'tenNhanVien': result[1],
                            'email': result[2],
                            'soDienThoai': result[3] if result[3] else '',
                            'role': result[4],
                            'maPhongBan': result[5],
                            'tenPhongBan': result[6] if result[6] else '',
                            'ngayTao': result[7].strftime('%Y-%m-%d %H:%M:%S') if result[7] else ''
                        },
                        'message': 'Lấy thông tin nhân viên thành công'
                    }
                else:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy nhân viên'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi lấy thông tin nhân viên: {str(e)}'
            }
    
    @staticmethod
    def create_nhanvien(ten_nhan_vien, email, password,ma_phong_ban, role='STAFF', so_dien_thoai=''):
        """
        Tạo nhân viên mới
        """
        try:
            with connection.cursor() as cursor:
                # Tạo mã nhân viên tự động
                cursor.execute("""
                    SELECT COUNT(*) + 1 FROM NhanVien
                """)
                count = cursor.fetchone()[0]
                ma_nhan_vien = f"NV{count:04d}"
                # Hash password
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                # Thêm nhân viên mới
                cursor.execute("""
                    INSERT INTO NhanVien (maNhanVien, tenNhanVien, email, password, soDienThoai, role, maPhongBan) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [ma_nhan_vien, ten_nhan_vien, email, password_hash, so_dien_thoai, role, ma_phong_ban])
                
                return {
                    'success': True,
                    'data': {
                        'maNhanVien': ma_nhan_vien,
                        'tenNhanVien': ten_nhan_vien,
                        'email': email,
                        'soDienThoai': so_dien_thoai,
                        'role': role,
                        'maPhongBan': ma_phong_ban
                    },
                    'message': 'Tạo nhân viên thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi tạo nhân viên: {str(e)}'
            }
    
    @staticmethod
    def update_nhanvien(ma_nhan_vien, ten_nhan_vien=None, email=None, password=None, so_dien_thoai=None, role=None, ma_phong_ban=None):
        """
        Cập nhật thông tin nhân viên
        """
        try:
            with connection.cursor() as cursor:
                # Kiểm tra nhân viên có tồn tại không
                cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE maNhanVien = %s", [ma_nhan_vien])
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy nhân viên'
                    }
                
                # Xây dựng câu lệnh UPDATE động
                update_fields = []
                update_values = []
                
                if ten_nhan_vien is not None:
                    update_fields.append("tenNhanVien = %s")
                    update_values.append(ten_nhan_vien)
                
                if email is not None:
                    update_fields.append("email = %s")
                    update_values.append(email)
                
                if password is not None:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    update_fields.append("password = %s")
                    update_values.append(password_hash)
                
                if so_dien_thoai is not None:
                    update_fields.append("soDienThoai = %s")
                    update_values.append(so_dien_thoai)
                
                if role is not None:
                    update_fields.append("role = %s")
                    update_values.append(role)
                
                if ma_phong_ban is not None:
                    update_fields.append("maPhongBan = %s")
                    update_values.append(ma_phong_ban)
                
                if not update_fields:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không có thông tin nào để cập nhật'
                    }
                
                # Thêm ma_nhan_vien vào cuối danh sách values
                update_values.append(ma_nhan_vien)
                
                # Thực hiện cập nhật
                sql = f"UPDATE NhanVien SET {', '.join(update_fields)} WHERE maNhanVien = %s"
                cursor.execute(sql, update_values)
                
                return {
                    'success': True,
                    'data': {
                        'maNhanVien': ma_nhan_vien
                    },
                    'message': 'Cập nhật nhân viên thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi cập nhật nhân viên: {str(e)}'
            }
    
    @staticmethod
    def delete_nhanvien(ma_nhan_vien):
        """
        Xóa nhân viên
        """
        try:
            with connection.cursor() as cursor:
                # Kiểm tra nhân viên có tồn tại không
                cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE maNhanVien = %s", [ma_nhan_vien])
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy nhân viên'
                    }
                
                # Xóa nhân viên
                cursor.execute("DELETE FROM NhanVien WHERE maNhanVien = %s", [ma_nhan_vien])
                
                return {
                    'success': True,
                    'data': {
                        'maNhanVien': ma_nhan_vien
                    },
                    'message': 'Xóa nhân viên thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi xóa nhân viên: {str(e)}'
            }
    
    @staticmethod
    def search_nhanvien(keyword):
        """
        Tìm kiếm nhân viên theo từ khóa
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nv.maNhanVien, nv.tenNhanVien, nv.email, nv.soDienThoai, 
                           nv.role, nv.maPhongBan, pb.tenPhongBan, nv.ngayTao
                    FROM NhanVien nv
                    LEFT JOIN PhongBan pb ON nv.maPhongBan = pb.maPhongBan
                    WHERE nv.tenNhanVien LIKE %s 
                       OR nv.email LIKE %s 
                       OR nv.maNhanVien LIKE %s
                       OR pb.tenPhongBan LIKE %s
                    ORDER BY nv.maNhanVien
                """, [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
                
                results = cursor.fetchall()
                
                nhanvien_list = []
                for row in results:
                    nhanvien_list.append({
                        'maNhanVien': row[0],
                        'tenNhanVien': row[1],
                        'email': row[2],
                        'soDienThoai': row[3] if row[3] else '',
                        'role': row[4],
                        'maPhongBan': row[5],
                        'tenPhongBan': row[6] if row[6] else '',
                        'ngayTao': row[7].strftime('%Y-%m-%d %H:%M:%S') if row[7] else ''
                    })
                
                return {
                    'success': True,
                    'data': nhanvien_list,
                    'message': f'Tìm thấy {len(nhanvien_list)} nhân viên'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi tìm kiếm nhân viên: {str(e)}'
            }
    
    @staticmethod
    def get_nhanvien_by_phongban(ma_phong_ban):
        """
        Lấy danh sách nhân viên theo phòng ban
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nv.maNhanVien, nv.tenNhanVien, nv.email, nv.soDienThoai, 
                           nv.role, nv.maPhongBan, pb.tenPhongBan, nv.ngayTao
                    FROM NhanVien nv
                    LEFT JOIN PhongBan pb ON nv.maPhongBan = pb.maPhongBan
                    WHERE nv.maPhongBan = %s
                    ORDER BY nv.maNhanVien
                """, [ma_phong_ban])
                
                results = cursor.fetchall()
                
                nhanvien_list = []
                for row in results:
                    nhanvien_list.append({
                        'maNhanVien': row[0],
                        'tenNhanVien': row[1],
                        'email': row[2],
                        'soDienThoai': row[3] if row[3] else '',
                        'role': row[4],
                        'maPhongBan': row[5],
                        'tenPhongBan': row[6] if row[6] else '',
                        'ngayTao': row[7].strftime('%Y-%m-%d %H:%M:%S') if row[7] else ''
                    })
                
                return {
                    'success': True,
                    'data': nhanvien_list,
                    'message': f'Lấy danh sách nhân viên phòng ban {ma_phong_ban} thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi lấy danh sách nhân viên theo phòng ban: {str(e)}'
            }
    
    @staticmethod
    def authenticate_nhanvien(email, password):
        """
        Xác thực nhân viên và trả về JWT token
        """
        try:
            with connection.cursor() as cursor:
                # Hash password để so sánh
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                cursor.execute("""
                    SELECT nv.maNhanVien, nv.tenNhanVien, nv.email, nv.soDienThoai, 
                           nv.role, nv.maPhongBan, pb.tenPhongBan, nv.ngayTao
                    FROM NhanVien nv
                    LEFT JOIN PhongBan pb ON nv.maPhongBan = pb.maPhongBan
                    WHERE nv.email = %s AND nv.password = %s
                """, [email, password_hash])
                
                result = cursor.fetchone()
                
                if result:
                    # Tạo user data
                    user_data = {
                        'maNhanVien': result[0],
                        'tenNhanVien': result[1],
                        'email': result[2],
                        'soDienThoai': result[3] if result[3] else '',
                        'role': result[4],
                        'maPhongBan': result[5],
                        'tenPhongBan': result[6] if result[6] else '',
                        'ngayTao': result[7].strftime('%Y-%m-%d %H:%M:%S') if result[7] else ''
                    }
                    
                    # Tạo JWT token
                    token_result = JWTUtils.generate_token(user_data)
                    
                    if token_result['success']:
                        return {
                            'success': True,
                            'data': {
                                'user': user_data,
                                'token': token_result['token'],
                                'expires_in': token_result['expires_in']
                            },
                            'message': 'Đăng nhập thành công'
                        }
                    else:
                        return {
                            'success': False,
                            'data': None,
                            'message': token_result['error']
                        }
                else:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Email hoặc mật khẩu không đúng'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi xác thực nhân viên: {str(e)}'
            }
