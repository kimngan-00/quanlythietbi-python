from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QuanLyThietBi.models.models import ThietBi, YeuCau, TrangThaiYC, TrangThaiTB
from django.db.models import F

# Helper function để tạo mã tự động
def get_next_code(prefix, model):
    last_object = model.objects.order_by('-pk').first()
    if not last_object:
        return f"{prefix}001"
    last_code = last_object.pk
    number = int(last_code.replace(prefix, '')) + 1
    return f"{prefix}{number:03}"

@api_view(['POST'])
def tao_thiet_bi(request):
    """ Tạo thiết bị mới """
    tenTB = request.data.get('tenTB')
    hangSX_id = request.data.get('hangSX')
    ttThietBi_id = request.data.get('ttThietBi')

    if not all([tenTB, hangSX_id, ttThietBi_id]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        maTB = get_next_code('TB', ThietBi)
        ThietBi.objects.create(
            maTB=maTB,
            tenTB=tenTB,
            hangSX_id=hangSX_id,
            ttThietBi_id=ttThietBi_id
        )
        return Response({"message": "Thiết bị đã được tạo thành công.", "maTB": maTB}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def cap_nhat_thiet_bi(request, ma_tb):
    """ Cập nhật thông tin thiết bị """
    try:
        thiet_bi = ThietBi.objects.get(maTB=ma_tb)
    except ThietBi.DoesNotExist:
        return Response({"error": "Không tìm thấy thiết bị."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    thiet_bi.tenTB = data.get('tenTB', thiet_bi.tenTB)
    thiet_bi.hangSX_id = data.get('hangSX', thiet_bi.hangSX_id)
    thiet_bi.ttThietBi_id = data.get('ttThietBi', thiet_bi.ttThietBi_id)
    thiet_bi.save()

    return Response({"message": "Thông tin thiết bị đã được cập nhật thành công."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def xem_danh_sach_thiet_bi_admin(request):
    """ Xem danh sách tất cả thiết bị """
    thiet_bi_list = ThietBi.objects.select_related('hangSX', 'ttThietBi').all()
    data = [{
        'maTB': tb.maTB,
        'tenTB': tb.tenTB,
        'hangSX': tb.hangSX.tenHang,
        'trangThai': tb.ttThietBi.tenTT
    } for tb in thiet_bi_list]
    return Response(data)

@api_view(['GET'])
def xem_nguoi_su_dung_thiet_bi(request):
    """ Xem danh sách người đang sử dụng thiết bị """
    users_with_devices = YeuCau.objects.filter(
        ttYeuCau__tenTT='approved'
    ).select_related('maNV', 'maTB')

    data = [{
        'maNhanVien': yc.maNV.maNhanVien,
        'tenNhanVien': yc.maNV.tenNhanVien,
        'email': yc.maNV.email,
        'maTB': yc.maTB.maTB,
        'tenTB': yc.maTB.tenTB
    } for yc in users_with_devices]
    return Response(data)

@api_view(['GET'])
def xem_danh_sach_yeu_cau(request):
    """ Xem danh sách tất cả yêu cầu """
    yeu_cau_list = YeuCau.objects.select_related('maNV', 'maTB', 'ttYeuCau').all()
    data = [{
        'maYC': yc.maYC,
        'maNhanVien': yc.maNV.maNhanVien,
        'tenNhanVien': yc.maNV.tenNhanVien,
        'maTB': yc.maTB.maTB,
        'tenTB': yc.maTB.tenTB,
        'trangThaiYeuCau': yc.ttYeuCau.tenTT
    } for yc in yeu_cau_list]
    return Response(data)

@api_view(['PUT'])
def phe_duyet_yeu_cau(request, ma_yc):
    """ Phê duyệt yêu cầu """
    try:
        yeu_cau = YeuCau.objects.get(maYC=ma_yc)
        approved_status = TrangThaiYC.objects.get(tenTT='approved')
        used_status = TrangThaiTB.objects.get(tenTT='used')

        # Kiểm tra nếu yêu cầu đang ở trạng thái 'wait'
        if yeu_cau.ttYeuCau.tenTT == 'wait':
            yeu_cau.ttYeuCau = approved_status
            yeu_cau.maTB.ttThietBi = used_status
            yeu_cau.save()
            yeu_cau.maTB.save()
            return Response({"message": "Yêu cầu đã được phê duyệt và trạng thái thiết bị đã cập nhật."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Chỉ có thể phê duyệt các yêu cầu đang chờ (wait)."}, status=status.HTTP_400_BAD_REQUEST)
    except YeuCau.DoesNotExist:
        return Response({"error": "Không tìm thấy yêu cầu."}, status=status.HTTP_404_NOT_FOUND)
    except TrangThaiYC.DoesNotExist:
        return Response({"error": "Không tìm thấy trạng thái 'approved'."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except TrangThaiTB.DoesNotExist:
        return Response({"error": "Không tìm thấy trạng thái 'used'."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)