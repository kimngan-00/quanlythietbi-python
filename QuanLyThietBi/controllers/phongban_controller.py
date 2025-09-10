from django.db import connection
from django.http import JsonResponse
import json

class PhongBanController:
    """
    Controller xử lý các thao tác với phòng ban
    """
    
    @staticmethod
    def get_phongban_list():
        """
        Lấy danh sách tất cả phòng ban
        """
        try:
            with connection.cursor() as cursor:
                # SQL query để lấy danh sách phòng ban
                cursor.execute("""
                    SELECT maPhongBan, tenPhongBan, moTa 
                    FROM PhongBan 
                    ORDER BY maPhongBan
                """)
                
                # Lấy tất cả kết quả
                results = cursor.fetchall()

                # Chuyển đổi thành danh sách dictionary
                phongban_list = []
                for row in results:
                    phongban_list.append({
                        'maPhongBan': row[0],
                        'tenPhongBan': row[1],
                        'moTa': row[2] if row[2] else ''
                    })
                
                return {
                    'success': True,
                    'data': phongban_list,
                    'message': 'Lấy danh sách phòng ban thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Lỗi khi lấy danh sách phòng ban: {str(e)}'
            }
    
    @staticmethod
    def get_phongban_by_id(ma_phong_ban):
        """
        Lấy thông tin phòng ban theo mã
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT maPhongBan, tenPhongBan, moTa 
                    FROM PhongBan 
                    WHERE maPhongBan = %s
                """, [ma_phong_ban])
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'success': True,
                        'data': {
                            'maPhongBan': result[0],
                            'tenPhongBan': result[1],
                            'moTa': result[2] if result[2] else ''
                        },
                        'message': 'Lấy thông tin phòng ban thành công'
                    }
                else:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy phòng ban'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi lấy thông tin phòng ban: {str(e)}'
            }
    
    @staticmethod
    def create_phongban(ten_phong_ban, mo_ta=None):
        """
        Tạo phòng ban mới
        """
        try:
            with connection.cursor() as cursor:
                # Tạo mã phòng ban tự động
                cursor.execute("""
                    SELECT COUNT(*) + 1 FROM PhongBan
                """)
                count = cursor.fetchone()[0]
                ma_phong_ban = f"PB{count:03d}"
                
                # Thêm phòng ban mới
                cursor.execute("""
                    INSERT INTO PhongBan (maPhongBan, tenPhongBan, moTa) 
                    VALUES (%s, %s, %s)
                """, [ma_phong_ban, ten_phong_ban, mo_ta])
                
                return {
                    'success': True,
                    'data': {
                        'maPhongBan': ma_phong_ban,
                        'tenPhongBan': ten_phong_ban,
                        'moTa': mo_ta
                    },
                    'message': 'Tạo phòng ban thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi tạo phòng ban: {str(e)}'
            }
    
    @staticmethod
    def update_phongban(ma_phong_ban, ten_phong_ban=None, mo_ta=None):
        """
        Cập nhật thông tin phòng ban
        """
        try:
            with connection.cursor() as cursor:
                # Kiểm tra phòng ban có tồn tại không
                cursor.execute("""
                    SELECT COUNT(*) FROM PhongBan WHERE maPhongBan = %s
                """, [ma_phong_ban])
                
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy phòng ban'
                    }
                
                # Cập nhật thông tin
                update_fields = []
                params = []
                
                if ten_phong_ban is not None:
                    update_fields.append("tenPhongBan = %s")
                    params.append(ten_phong_ban)
                
                if mo_ta is not None:
                    update_fields.append("moTa = %s")
                    params.append(mo_ta)
                
                if update_fields:
                    params.append(ma_phong_ban)
                    cursor.execute(f"""
                        UPDATE PhongBan 
                        SET {', '.join(update_fields)}
                        WHERE maPhongBan = %s
                    """, params)
                
                return {
                    'success': True,
                    'data': {'maPhongBan': ma_phong_ban},
                    'message': 'Cập nhật phòng ban thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi cập nhật phòng ban: {str(e)}'
            }
    
    @staticmethod
    def delete_phongban(ma_phong_ban):
        """
        Xóa phòng ban
        """
        try:
            with connection.cursor() as cursor:
                # Kiểm tra phòng ban có tồn tại không
                cursor.execute("""
                    SELECT COUNT(*) FROM PhongBan WHERE maPhongBan = %s
                """, [ma_phong_ban])
                
                if cursor.fetchone()[0] == 0:
                    return {
                        'success': False,
                        'data': None,
                        'message': 'Không tìm thấy phòng ban'
                    }
                
                # Xóa phòng ban
                cursor.execute("""
                    DELETE FROM PhongBan WHERE maPhongBan = %s
                """, [ma_phong_ban])
                
                return {
                    'success': True,
                    'data': {'maPhongBan': ma_phong_ban},
                    'message': 'Xóa phòng ban thành công'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Lỗi khi xóa phòng ban: {str(e)}'
            }
    
    @staticmethod
    def search_phongban(keyword):
        """
        Tìm kiếm phòng ban theo từ khóa
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT maPhongBan, tenPhongBan, moTa 
                    FROM PhongBan 
                    WHERE tenPhongBan LIKE %s OR moTa LIKE %s
                    ORDER BY maPhongBan
                """, [f'%{keyword}%', f'%{keyword}%'])
                
                results = cursor.fetchall()
                
                phongban_list = []
                for row in results:
                    phongban_list.append({
                        'maPhongBan': row[0],
                        'tenPhongBan': row[1],
                        'moTa': row[2] if row[2] else ''
                    })
                
                return {
                    'success': True,
                    'data': phongban_list,
                    'message': f'Tìm thấy {len(phongban_list)} phòng ban'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Lỗi khi tìm kiếm phòng ban: {str(e)}'
            } 