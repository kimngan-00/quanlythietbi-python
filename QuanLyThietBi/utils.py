import jwt
from datetime import datetime, timedelta
from django.conf import settings

class JWTUtils:
    """
    Utility class để xử lý JWT tokens
    """
    
    # Secret key cho JWT
    SECRET_KEY = getattr(settings, 'SECRET_KEY', 'your-secret-key-here')
    
    # Thời gian hết hạn của token (24 giờ)
    EXPIRATION_TIME = timedelta(hours=24)
    
    @classmethod
    def generate_token(cls, user_data):
        """
        Tạo JWT token từ thông tin user
        """
        try:
            # Payload chứa thông tin user
            payload = {
                'maNhanVien': user_data['maNhanVien'],
                'email': user_data['email'],
                'role': user_data['role'],
                'maPhongBan': user_data['maPhongBan'],
                'iat': datetime.utcnow(),  # Issued at
                'exp': datetime.utcnow() + cls.EXPIRATION_TIME  # Expiration time
            }
            
            # Tạo token
            token = jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')
            
            return {
                'success': True,
                'token': token,
                'expires_in': int(cls.EXPIRATION_TIME.total_seconds())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Lỗi khi tạo token: {str(e)}'
            }
    
    @classmethod
    def verify_token(cls, token):
        """
        Xác thực JWT token
        """
        try:
            # Decode token
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            
            return {
                'success': True,
                'data': payload
            }
            
        except jwt.ExpiredSignatureError:
            return {
                'success': False,
                'error': 'Token đã hết hạn'
            }
        except jwt.InvalidTokenError:
            return {
                'success': False,
                'error': 'Token không hợp lệ'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Lỗi khi xác thực token: {str(e)}'
            }
