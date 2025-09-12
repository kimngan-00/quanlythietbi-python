from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..controllers.nhanvien_controller import NhanVienController


@csrf_exempt
@require_http_methods(["GET"])
def get_nhanvien_list(request):
    """
    API endpoint lấy danh sách nhân viên
    """
    try:
        # Sử dụng controller để lấy danh sách nhân viên
        result = NhanVienController.get_nhanvien_list()

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=500
            )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["GET"])
def get_nhanvien_by_id(request, ma_nhan_vien):
    """
    API endpoint lấy thông tin nhân viên theo mã
    """
    try:
        result = NhanVienController.get_nhanvien_by_id(ma_nhan_vien)

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=404
            )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
def create_nhanvien(request):
    """
    API endpoint tạo nhân viên mới
    """
    try:
        data = json.loads(request.body)
        ten_nhan_vien = data.get("tenNhanVien")
        email = data.get("email")
        password = data.get("password")
        so_dien_thoai = data.get("soDienThoai", "")
        role = data.get("role", "STAFF")
        ma_phong_ban = data.get("maPhongBan")
        print("role: ------------------------------", role)
        if not ten_nhan_vien:
            return JsonResponse(
                {"success": False, "message": "Tên nhân viên không được để trống"},
                status=400,
            )

        if not email:
            return JsonResponse(
                {"success": False, "message": "Email không được để trống"}, status=400
            )

        if not ma_phong_ban:
            return JsonResponse(
                {"success": False, "message": "Mã phòng ban không được để trống"},
                status=400,
            )

        result = NhanVienController.create_nhanvien(
            ten_nhan_vien, email, password, ma_phong_ban, role, so_dien_thoai
        )

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=201,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=500
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dữ liệu JSON không hợp lệ"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["PUT"])
def update_nhanvien(request, ma_nhan_vien):
    """
    API endpoint cập nhật nhân viên
    """
    try:
        data = json.loads(request.body)
        ten_nhan_vien = data.get("tenNhanVien")
        email = data.get("email")
        so_dien_thoai = data.get("soDienThoai")
        role = data.get("role")
        ma_phong_ban = data.get("maPhongBan")

        result = NhanVienController.update_nhanvien(
            ma_nhan_vien, ten_nhan_vien, email, so_dien_thoai, role, ma_phong_ban
        )

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=404
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dữ liệu JSON không hợp lệ"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_nhanvien(request, ma_nhan_vien):
    """
    API endpoint xóa nhân viên
    """
    try:
        result = NhanVienController.delete_nhanvien(ma_nhan_vien)

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=404
            )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["GET"])
def search_nhanvien(request):
    """
    API endpoint tìm kiếm nhân viên
    """
    try:
        keyword = request.GET.get("keyword", "")

        if not keyword:
            return JsonResponse(
                {"success": False, "message": "Từ khóa tìm kiếm không được để trống"},
                status=400,
            )

        result = NhanVienController.search_nhanvien(keyword)

        return JsonResponse(
            {
                "success": result["success"],
                "data": result["data"],
                "message": result["message"],
            },
            status=200,
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["GET"])
def get_nhanvien_by_phongban(request, ma_phong_ban):
    """
    API endpoint lấy danh sách nhân viên theo phòng ban
    """
    try:
        result = NhanVienController.get_nhanvien_by_phongban(ma_phong_ban)

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=500
            )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
def authenticate_nhanvien(request):
    """
    API endpoint xác thực nhân viên (đăng nhập)
    """
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse(
                {"success": False, "message": "Email và mật khẩu không được để trống"},
                status=400,
            )

        result = NhanVienController.authenticate_nhanvien(email, password)

        if result["success"]:
            return JsonResponse(
                {"success": True, "data": result["data"], "message": result["message"]},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": result["message"]}, status=401
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dữ liệu JSON không hợp lệ"}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Lỗi server: {str(e)}"}, status=500
        )
