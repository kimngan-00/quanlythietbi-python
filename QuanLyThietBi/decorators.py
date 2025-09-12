from functools import wraps
from django.http import JsonResponse
from .utils import JWTUtils

def jwt_required(view_func):
    """
    Decorator để yêu cầu JWT token cho các API
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Lấy token từ header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return JsonResponse({
                'success': False,
                'message': 'Unauthorized'
            }, status=401)
        
        # Kiểm tra format "Bearer <token>"
        try:
            token = auth_header.split(' ')[1]  # Lấy phần token sau "Bearer "
        except IndexError:
            return JsonResponse({
                'success': False,
                'message': 'Format token không đúng. Sử dụng: Bearer <token>'
            }, status=401)
        
        # Xác thực token
        result = JWTUtils.verify_token(token)
        
        if not result['success']:
            return JsonResponse({
                'success': False,
                'message': result['error']
            }, status=401)
        
        # Thêm thông tin user vào request
        request.user_info = result['data']
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def admin_required(view_func):
    """
    Decorator để yêu cầu quyền admin
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Kiểm tra JWT token trước
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return JsonResponse({
                'success': False,
                'message': 'Unauthorized'
            }, status=401)
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return JsonResponse({
                'success': False,
                'message': 'Format token không đúng'
            }, status=401)
        
        result = JWTUtils.verify_token(token)
        
        if not result['success']:
            return JsonResponse({
                'success': False,
                'message': result['error']
            }, status=401)
        
        # Kiểm tra quyền admin
        if result['data']['role'] != 'ADMIN':
            return JsonResponse({
                'success': False,
                'message': 'Bạn không có quyền truy cập'
            }, status=403)
        
        request.user_info = result['data']
        return view_func(request, *args, **kwargs)
    
    return wrapper

def check_role(required_roles):
    """
    Decorator để kiểm tra role cụ thể
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Kiểm tra JWT token trước
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            
            if not auth_header:
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized'
                }, status=401)
            
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return JsonResponse({
                    'success': False,
                    'message': 'Format token không đúng'
                }, status=401)
            
            result = JWTUtils.verify_token(token)
            
            if not result['success']:
                return JsonResponse({
                    'success': False,
                    'message': result['error']
                }, status=401)
            
            # Kiểm tra role
            user_role = result['data']['role']
            if user_role not in required_roles:
                return JsonResponse({
                    'success': False,
                    'message': f'Bạn cần quyền {", ".join(required_roles)} để truy cập'
                }, status=403)
            
            request.user_info = result['data']
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
