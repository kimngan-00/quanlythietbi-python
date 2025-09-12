from django.db import models
from .phongban import PhongBan

class NhanVien(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Nhân viên'),
    ]
    
    maNhanVien = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="Mã nhân viên"
    )
    tenNhanVien = models.CharField(
        max_length=255,
        verbose_name="Tên nhân viên",
        help_text="Họ và tên nhân viên"
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email",
        help_text="Địa chỉ email của nhân viên"
    )
    soDienThoai = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Số điện thoại",
        help_text="Số điện thoại liên lạc"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STAFF',
        verbose_name="Vai trò",
        help_text="Vai trò của nhân viên trong hệ thống"
    )
    maPhongBan = models.ForeignKey(
        PhongBan,
        on_delete=models.CASCADE,
        db_column='maPhongBan',
        verbose_name="Mã phòng ban",
        help_text="Phòng ban mà nhân viên thuộc về"
    )
    ngayTao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo",
        help_text="Ngày tạo hồ sơ nhân viên"
    )
    
    class Meta:
        db_table = 'NhanVien'
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['maNhanVien']
        managed = True
    
    def __str__(self):
        return f"{self.maNhanVien} - {self.tenNhanVien}"
    
    def save(self, *args, **kwargs):
        # Tự động tạo mã nhân viên nếu chưa có
        if not self.maNhanVien:
            # Lấy số lượng nhân viên hiện tại và tạo mã mới
            count = NhanVien.objects.count() + 1
            self.maNhanVien = f"NV{count:04d}"
        super().save(*args, **kwargs)
    
    @classmethod
    def create_table_if_not_exists(cls):
        """Tạo bảng nếu chưa tồn tại"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Kiểm tra bảng đã tồn tại chưa
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'NhanVien'
            """)
            
            if cursor.fetchone()[0] == 0:
                # Tạo bảng nếu chưa tồn tại
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS NhanVien (
                        maNhanVien VARCHAR(20) PRIMARY KEY,
                        tenNhanVien VARCHAR(255) 
                            CHARACTER SET utf8mb4 
                            COLLATE utf8mb4_0900_ai_ci NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        soDienThoai VARCHAR(20),
                        role ENUM('ADMIN', 'STAFF') NOT NULL DEFAULT 'STAFF',
                        maPhongBan VARCHAR(20) NOT NULL,
                        ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT fk_phongban FOREIGN KEY (maPhongBan) REFERENCES PhongBan(maPhongBan)
                    ) 
                    CHARACTER SET = utf8mb4 
                    COLLATE = utf8mb4_0900_ai_ci
                """)
                print("Đã tạo bảng NhanVien thành công!")
            else:
                print("Bảng NhanVien đã tồn tại!")
