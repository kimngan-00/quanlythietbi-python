from django.db import models

class PhongBan(models.Model):
    maPhongBan = models.CharField(
        max_length=20, 
        primary_key=True,
        verbose_name="Mã phòng ban"
    )
    tenPhongBan = models.CharField(
        max_length=255,
        verbose_name="Tên phòng ban",
        help_text="Tên của phòng ban"
    )
    moTa = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mô tả",
        help_text="Mô tả chi tiết về phòng ban"
    )
    
    class Meta:
        db_table = 'PhongBan'
        verbose_name = "Phòng ban"
        verbose_name_plural = "Phòng ban"
        ordering = ['maPhongBan']
        # Thêm option để tạo bảng với IF NOT EXISTS
        managed = True
    
    def __str__(self):
        return f"{self.maPhongBan} - {self.tenPhongBan}"
    
    def save(self, *args, **kwargs):
        # Tự động tạo mã phòng ban nếu chưa có
        if not self.maPhongBan:
            # Lấy số lượng phòng ban hiện tại và tạo mã mới
            count = PhongBan.objects.count() + 1
            self.maPhongBan = f"PB{count:03d}"
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
                AND table_name = 'PhongBan'
            """)
            
            if cursor.fetchone()[0] == 0:
                # Tạo bảng nếu chưa tồn tại
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PhongBan (
                        maPhongBan VARCHAR(20) PRIMARY KEY,
                        tenPhongBan VARCHAR(255) 
                            CHARACTER SET utf8mb4 
                            COLLATE utf8mb4_0900_ai_ci NOT NULL,
                        moTa TEXT 
                            CHARACTER SET utf8mb4 
                            COLLATE utf8mb4_0900_ai_ci
                    ) 
                    CHARACTER SET = utf8mb4 
                    COLLATE = utf8mb4_0900_ai_ci
                """)
                print("✅ Đã tạo bảng PhongBan thành công!")
            else:
                print("ℹ️ Bảng PhongBan đã tồn tại!")
