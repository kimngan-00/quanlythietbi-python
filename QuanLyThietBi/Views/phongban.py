from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..controllers.phongban_controller import PhongBanController

@csrf_exempt
@require_http_methods(["GET"])
def get_phongban_list(request):
    """
    API endpoint lấy danh sách phòng ban
    """
    try:
        # Sử dụng controller để lấy danh sách phòng ban
        result = PhongBanController.get_phongban_list()
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_phongban_by_id(request, ma_phong_ban):
    """
    API endpoint lấy thông tin phòng ban theo mã
    """
    try:
        result = PhongBanController.get_phongban_by_id(ma_phong_ban)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_phongban(request):
    """
    API endpoint tạo phòng ban mới
    """
    try:
        data = json.loads(request.body)
        ten_phong_ban = data.get('tenPhongBan')
        mo_ta = data.get('moTa', '')
        
        if not ten_phong_ban:
            return JsonResponse({
                'success': False,
                'message': 'Tên phòng ban không được để trống'
            }, status=400)
        
        result = PhongBanController.create_phongban(ten_phong_ban, mo_ta)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu JSON không hợp lệ'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_phongban(request, ma_phong_ban):
    """
    API endpoint cập nhật phòng ban
    """
    try:
        data = json.loads(request.body)
        ten_phong_ban = data.get('tenPhongBan')
        mo_ta = data.get('moTa')
        
        result = PhongBanController.update_phongban(ma_phong_ban, ten_phong_ban, mo_ta)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu JSON không hợp lệ'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_phongban(request, ma_phong_ban):
    """
    API endpoint xóa phòng ban
    """
    try:
        result = PhongBanController.delete_phongban(ma_phong_ban)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data'],
                'message': result['message']
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def search_phongban(request):
    """
    API endpoint tìm kiếm phòng ban
    """
    try:
        keyword = request.GET.get('keyword', '')
        
        if not keyword:
            return JsonResponse({
                'success': False,
                'message': 'Từ khóa tìm kiếm không được để trống'
            }, status=400)
        
        result = PhongBanController.search_phongban(keyword)
        
        return JsonResponse({
            'success': result['success'],
            'data': result['data'],
            'message': result['message']
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }, status=500)
