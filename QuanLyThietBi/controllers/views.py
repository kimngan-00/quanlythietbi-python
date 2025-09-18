from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.models import ThietBi, YeuCau, NhanVien, TrangThaiTB, TrangThaiYC, HangSX

# Endpoint chung cho cả Admin và Nhân viên
@api_view(['GET'])
def list_all_devices(request):
    """
    Lấy danh sách tất cả thiết bị
    """
    devices = ThietBi.objects.all().select_related('hangSX', 'ttThietBi')
    data = [{
        'maTB': d.maTB,
        'tenTB': d.tenTB,
        'hangSX': d.hangSX.tenHang,
        'ttThietBi': d.ttThietBi.tenTT
    } for d in devices]
    return Response(data)

# --- Chức năng của ADMIN ---

@api_view(['POST'])
def create_device(request):
    """
    Tạo thiết bị mới
    """
    data = request.data
    try:
        # Lấy các đối tượng HangSX và TrangThaiTB dựa vào mã
        hangSX_obj = HangSX.objects.get(maHang=data.get('hangSX'))
        ttThietBi_obj = TrangThaiTB.objects.get(maTT=data.get('ttThietBi'))

        new_device = ThietBi.objects.create(
            maTB=data.get('maTB'),
            tenTB=data.get('tenTB'),
            hangSX=hangSX_obj,
            ttThietBi=ttThietBi_obj
        )
        return Response({'message': 'Thiết bị đã được tạo thành công.', 'data': {'maTB': new_device.maTB, 'tenTB': new_device.tenTB}}, status=status.HTTP_201_CREATED)
    except HangSX.DoesNotExist:
        return Response({'error': 'Không tìm thấy hãng sản xuất.'}, status=status.HTTP_404_NOT_FOUND)
    except TrangThaiTB.DoesNotExist:
        return Response({'error': 'Không tìm thấy trạng thái thiết bị.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_device(request, maTB):
    """
    Cập nhật thông tin thiết bị
    """
    data = request.data
    try:
        device = ThietBi.objects.get(maTB=maTB)
        device.tenTB = data.get('tenTB', device.tenTB)
        if 'hangSX' in data:
            hangSX_obj = HangSX.objects.get(maHang=data.get('hangSX'))
            device.hangSX = hangSX_obj
        if 'ttThietBi' in data:
            ttThietBi_obj = TrangThaiTB.objects.get(maTT=data.get('ttThietBi'))
            device.ttThietBi = ttThietBi_obj
        device.save()
        return Response({'message': 'Thông tin thiết bị đã được cập nhật.'}, status=status.HTTP_200_OK)
    except ThietBi.DoesNotExist:
        return Response({'error': 'Không tìm thấy thiết bị'}, status=status.HTTP_404_NOT_FOUND)
    except HangSX.DoesNotExist:
        return Response({'error': 'Không tìm thấy hãng sản xuất.'}, status=status.HTTP_404_NOT_FOUND)
    except TrangThaiTB.DoesNotExist:
        return Response({'error': 'Không tìm thấy trạng thái thiết bị.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_devices_in_use(request):
    """
    Xem danh sách người đang sử dụng thiết bị
    """
    used_devices = YeuCau.objects.filter(ttYeuCau__tenTT='approved').select_related('maTB', 'maNV')
    data = [{
        'maTB': yc.maTB.maTB,
        'tenTB': yc.maTB.tenTB,
        'nguoiSuDung': yc.maNV.tenNhanVien,
        'maYC': yc.maYC
    } for yc in used_devices]
    return Response(data)

@api_view(['GET'])
def list_all_requests(request):
    """
    Xem danh sách tất cả yêu cầu
    """
    requests = YeuCau.objects.all().select_related('maNV', 'maTB', 'ttYeuCau')
    data = [{
        'maYC': yc.maYC,
        'maNV': yc.maNV.maNhanVien,
        'tenNV': yc.maNV.tenNhanVien,
        'maTB': yc.maTB.maTB,
        'tenTB': yc.maTB.tenTB,
        'trangThaiYeuCau': yc.ttYeuCau.tenTT
    } for yc in requests]
    return Response(data)

@api_view(['PUT'])
def approve_request(request, maYC):
    """
    Phê duyệt yêu cầu
    """
    try:
        request_obj = YeuCau.objects.get(maYC=maYC)
        approved_status = TrangThaiYC.objects.get(tenTT='approved')
        request_obj.ttYeuCau = approved_status
        request_obj.save()

        # Cập nhật trạng thái của thiết bị sau khi phê duyệt
        used_status = TrangThaiTB.objects.get(tenTT='used')
        request_obj.maTB.ttThietBi = used_status
        request_obj.maTB.save()

        return Response({'message': f'Yêu cầu {maYC} đã được phê duyệt.'}, status=status.HTTP_200_OK)
    except YeuCau.DoesNotExist:
        return Response({'error': 'Không tìm thấy yêu cầu'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def reject_request(request, maYC):
    """
    Từ chối yêu cầu
    """
    try:
        request_obj = YeuCau.objects.get(maYC=maYC)
        reject_status = TrangThaiYC.objects.get(tenTT='reject')
        request_obj.ttYeuCau = reject_status
        request_obj.save()
        return Response({'message': f'Yêu cầu {maYC} đã bị từ chối.'}, status=status.HTTP_200_OK)
    except YeuCau.DoesNotExist:
        return Response({'error': 'Không tìm thấy yêu cầu'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# --- Chức năng của Nhân viên ---

@api_view(['POST'])
def create_request(request):
    """
    Tạo yêu cầu mượn thiết bị, maYC được sinh tự động
    """
    data = request.data
    ma_thiet_bi = data.get('maTB')
    # Hardcode maNV là NV0001
    ma_nhan_vien = 'NV0001'

    try:
        device = ThietBi.objects.get(maTB=ma_thiet_bi)
        # Kiểm tra trạng thái thiết bị là 'free' (mã 2)
        if device.ttThietBi.maTT != 2:
            return Response({'error': 'Thiết bị không sẵn sàng để yêu cầu. Vui lòng chọn thiết bị khác.'}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy đối tượng nhân viên
        nhan_vien = NhanVien.objects.get(maNhanVien=ma_nhan_vien)
        # Lấy đối tượng trạng thái 'wait'
        wait_status = TrangThaiYC.objects.get(tenTT='wait')

        # === LOGIC MỚI: TẠO MÃ YÊU CẦU TỰ ĐỘNG ===
        last_request = YeuCau.objects.order_by('-maYC').first()
        if last_request:
            last_number = int(last_request.maYC[2:])
            new_number = last_number + 1
            new_maYC = f"YC{new_number:03d}"
        else:
            new_maYC = "YC001"
        # ==========================================

        # Tạo yêu cầu
        YeuCau.objects.create(
            maYC=new_maYC,
            maNV=nhan_vien,
            maTB=device,
            ttYeuCau=wait_status
        )

        # Cập nhật trạng thái của thiết bị thành 'maintenance' (bảo trì) sau khi có yêu cầu
        maintenance_status = TrangThaiTB.objects.get(tenTT='maintenance')
        device.ttThietBi = maintenance_status
        device.save()

        return Response({'message': f'Yêu cầu {new_maYC} đã được tạo thành công, đang chờ phê duyệt.'}, status=status.HTTP_201_CREATED)
    except ThietBi.DoesNotExist:
        return Response({'error': 'Không tìm thấy thiết bị'}, status=status.HTTP_404_NOT_FOUND)
    except NhanVien.DoesNotExist:
        return Response({'error': 'Không tìm thấy nhân viên'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_my_requests(request):
    """
    Xem danh sách yêu cầu của nhân viên (hardcode NV0001)
    """
    ma_nhan_vien = 'NV0001'
    try:
        requests = YeuCau.objects.filter(maNV__maNhanVien=ma_nhan_vien).select_related('maTB', 'ttYeuCau')
        data = [{
            'maYC': yc.maYC,
            'maTB': yc.maTB.maTB,
            'tenTB': yc.maTB.tenTB,
            'trangThaiYeuCau': yc.ttYeuCau.tenTT
        } for yc in requests]
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)