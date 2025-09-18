from django.db import models

class PhongBan(models.Model):
    maPhongBan = models.CharField(primary_key=True, max_length=20)
    tenPhongBan = models.CharField(max_length=255)
    moTa = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'PhongBan'
        verbose_name_plural = 'PhongBan'

class HangSX(models.Model):
    maHang = models.CharField(primary_key=True, max_length=5)
    tenHang = models.CharField(max_length=50)

    class Meta:
        db_table = 'HangSX'
        verbose_name_plural = 'HangSX'

class TrangThaiTB(models.Model):
    maTT = models.IntegerField(primary_key=True)
    tenTT = models.CharField(max_length=50)

    class Meta:
        db_table = 'TrangThaiTB'
        verbose_name_plural = 'TrangThaiTB'

class TrangThaiYC(models.Model):
    maTT = models.IntegerField(primary_key=True)
    tenTT = models.CharField(max_length=50)

    class Meta:
        db_table = 'TrangThaiYC'
        verbose_name_plural = 'TrangThaiYC'

class NhanVien(models.Model):
    maNhanVien = models.CharField(primary_key=True, max_length=20)
    tenNhanVien = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    soDienThoai = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=[('ADMIN', 'Admin'), ('STAFF', 'Staff')], default='STAFF')
    maPhongBan = models.ForeignKey(PhongBan, on_delete=models.CASCADE, db_column='maPhongBan')
    ngayTao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'NhanVien'
        verbose_name_plural = 'NhanVien'

class ThietBi(models.Model):
    maTB = models.CharField(primary_key=True, max_length=5)
    tenTB = models.CharField(max_length=50)
    hangSX = models.ForeignKey(HangSX, on_delete=models.CASCADE, db_column='hangSX')
    ttThietBi = models.ForeignKey(TrangThaiTB, on_delete=models.CASCADE, db_column='ttThietBi')

    class Meta:
        db_table = 'ThietBi'
        verbose_name_plural = 'ThietBi'

class YeuCau(models.Model):
    maYC = models.CharField(primary_key=True, max_length=5)
    maNV = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='maNV')
    maTB = models.ForeignKey(ThietBi, on_delete=models.CASCADE, db_column='maTB')
    ttYeuCau = models.ForeignKey(TrangThaiYC, on_delete=models.CASCADE, db_column='ttYeuCau')

    class Meta:
        db_table = 'YeuCau'
        verbose_name_plural = 'YeuCau'