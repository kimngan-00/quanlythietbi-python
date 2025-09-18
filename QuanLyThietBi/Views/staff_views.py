from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from QuanLyThietBi.models.models import ThietBi, YeuCau, TrangThaiYC
from django.db.models import F


# Helper function để tạo mã tự động
def get_next_code(prefix, model):
    last_object = model.objects.order_by('-pk').first()
    if not last_object:
        return f"{prefix}001"
    last_code = last_object.pk
    number = int(last_code.replace(prefix, '')) + 1
    return f"{prefix}{number:03}"


@api_view(['GET'])
def xem_danh_sach_thiet_bi_staff(request):
    """ Xem danh sách tất cả thiết bị (dành cho nhân viên) """
    thiet_bi_list = ThietBi.objects.select_related('hangSX', 'ttThietBi').all()
    data = [{
        'maTB': tb.maTB,
        'tenTB': tb.tenTB,
        'hangSX': tb.hangSX.tenHang,
        'trangThai': tb.ttThietBi.tenTT
    } for tb in thiet_bi_list]
    return Response(data)


@api_view(['POST'])
def tao_yeu_cau(request):
    """ Tạo yêu cầu mượn thiết bị """
    ma_tb = request.data.get('maTB')

    # Mã nhân viên được hardcode như yêu cầu
    ma_nv = "NV0001"

    try:
        thiet_bi = ThietBi.objects.select_related('ttThietBi').get(maTB=ma_tb)
        wait_status = TrangThaiYC.objects.get(tenTT='wait')
        free_status_id = 2  # id của trạng thái 'free'

        # Kiểm tra trạng thái thiết bị có phải là 'free' không
        if thiet_bi.ttThietBi.tenTT.lower() != 'free':
            return Response({"error": "Thiết bị này không có sẵn để tạo yêu cầu."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem đã có yêu cầu 'wait' nào cho thiết bị này chưa
        if YeuCau.objects.filter(maTB=thiet_bi, ttYeuCau__tenTT='wait').exists():
            return Response({"error": "Thiết bị này đã có yêu cầu đang chờ phê duyệt."},
                            status=status.HTTP_400_BAD_REQUEST)

        ma_yc = get_next_code('YC', YeuCau)
        YeuCau.objects.create(
            maYC=ma_yc,
            maNV_id=ma_nv,
            maTB_id=ma_tb,
            ttYeuCau=wait_status
        )
        return Response({"message": "Yêu cầu đã được tạo thành công.", "maYC": ma_yc}, status=status.HTTP_201_CREATED)
    except ThietBi.DoesNotExist:
        return Response({"error": "Không tìm thấy thiết bị."}, status=status.HTTP_404_NOT_FOUND)
    except TrangThaiYC.DoesNotExist:
        return Response({"error": "Không tìm thấy trạng thái 'wait'"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)