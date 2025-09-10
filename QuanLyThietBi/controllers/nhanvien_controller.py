from django.db import connection
from django.http import JsonResponse
import json

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
                print('results: ------------------------------', results)
                
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
                'data': [],
                'message': f'Lỗi khi lấy danh sách nhân viên: {str(e)}'
            }
    
    @staticmethod
    def get_nhanvien_by_id(ma_nhan_vien):
        """
        Lấy thông tin nhân viên theo mã
        """
        print('ma_nhan_vien: ------------------------------', ma_nhan_vien)
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
    def create_nhanvien(ten_nhan_vien, email, so_dien_thoai=None, role='STAFF', ma_phong_ban=None):
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
                
                # Thêm nhân viên mới
                cursor.execute("""
                    INSERT INTO NhanVien (maNhanVien, tenNhanVien, email, soDienThoai, role, maPhongBan) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [ma_nhan_vien, ten_nhan_vien, email, so_dien_thoai, role, ma_phong_ban])
                
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
    def update_nhanvien(ma_nhan_vien, ten_nhan_vien=None, email=None, so_dien_thoai=None, role=None, ma_phong_ban=None):
        """
        Cập nhật thông tin nhân viên
        """
        try:
            with connection.cursor() as cursor:
                # Kiểm tra nhân viên có tồn tại không
                cursor.execute("""
                    SELECT COUNT(*) FROM NhanVien WHERE maNhanVien = %s
                """, [ma_nhan_vien])
                
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy nhân viên'
                    }
                
                # Cập nhật thông tin
                update_fields = []
                params = []
                
                if ten_nhan_vien is not None:
                    update_fields.append("tenNhanVien = %s")
                    params.append(ten_nhan_vien)
                
                if email is not None:
                    update_fields.append("email = %s")
                    params.append(email)
                
                if so_dien_thoai is not None:
                    update_fields.append("soDienThoai = %s")
                    params.append(so_dien_thoai)
                
                if role is not None:
                    update_fields.append("role = %s")
                    params.append(role)
                
                if ma_phong_ban is not None:
                    update_fields.append("maPhongBan = %s")
                    params.append(ma_phong_ban)
                
                if update_fields:
                    params.append(ma_nhan_vien)
                    cursor.execute(f"""
                        UPDATE NhanVien 
                        SET {', '.join(update_fields)}
                        WHERE maNhanVien = %s
                    """, params)
                
                return {
                    'success': True,
                    'data': {'maNhanVien': ma_nhan_vien},
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
                cursor.execute("""
                    SELECT COUNT(*) FROM NhanVien WHERE maNhanVien = %s
                """, [ma_nhan_vien])
                
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy nhân viên'
                    }
                
                # Xóa nhân viên
                cursor.execute("""
                    DELETE FROM NhanVien WHERE maNhanVien = %s
                """, [ma_nhan_vien])
                
                return {
                    'success': True,
                    'data': {'maNhanVien': ma_nhan_vien},
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
                    WHERE nv.tenNhanVien LIKE %s OR nv.email LIKE %s OR pb.tenPhongBan LIKE %s
                    ORDER BY nv.maNhanVien
                """, [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
                
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
                'data': [],
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
                    'message': f'Lấy danh sách nhân viên phòng ban thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Lỗi khi lấy danh sách nhân viên phòng ban: {str(e)}'
            }
