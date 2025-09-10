import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Kết nối đến MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=os.getenv('MYSQL_DATABASE', 'quanlythietbi'),
                port=os.getenv('MYSQL_PORT', 3306),
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("✅ Kết nối MySQL thành công!")
                return True
                
        except Error as e:
            print(f"❌ Lỗi kết nối MySQL: {e}")
            return False
    
    def disconnect(self):
        """Đóng kết nối MySQL"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Đã đóng kết nối MySQL")
    
    def execute_query(self, query, params=None):
        """Thực thi câu lệnh SQL"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params)
            
            # Nếu là SELECT query
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                # Nếu là INSERT, UPDATE, DELETE
                self.connection.commit()
                return self.cursor.rowcount
                
        except Error as e:
            print(f"❌ Lỗi thực thi query: {e}")
            return None
    
# Hàm tiện ích để test kết nối
def test_connection():
    """Test kết nối MySQL"""
    db = MySQLConnection()
    
    if db.connect():
        # Test các chức năng cơ bản
        print("\n🔍 Testing MySQL connection...")
        
        # Hiển thị databases
        db.show_databases()
        
        # Hiển thị tables
        db.show_tables()
        
        # Test query đơn giản
        result = db.execute_query("SELECT VERSION()")
        if result:
            print(f"📊 MySQL Version: {result[0][0]}")
        
        db.disconnect()
        return True
    else:
        return False

if __name__ == "__main__":
    # Test kết nối
    print("🚀 Bắt đầu test kết nối MySQL...")
    test_connection()
