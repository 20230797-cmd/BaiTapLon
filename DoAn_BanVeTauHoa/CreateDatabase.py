import pyodbc

# THÔNG SỐ KẾT NỐI (Lấy chuẩn từ ảnh của bạn)
SERVER = r'localhost\SQLEXPRESS'
DATABASE = 'QuanLyTauHoa_MSSQL'
# Sử dụng Windows Authentication (Trust Server Certificate)
CONNECTION_STRING = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

def tao_csdl_mssql():
    try:
        print("Đang kết nối đến SQL Server...")
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # 1. Bảng Tài khoản
        cursor.execute('''IF OBJECT_ID('tai_khoan', 'U') IS NULL 
                          CREATE TABLE tai_khoan (username NVARCHAR(50) PRIMARY KEY, password NVARCHAR(50), vai_tro NVARCHAR(20) DEFAULT 'user')''')
        
        # Thêm Admin gốc (Dùng TRY CATCH để không báo lỗi nếu đã có)
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM tai_khoan WHERE username='admin')
            INSERT INTO tai_khoan (username, password, vai_tro) VALUES ('admin', '123456', 'admin')
        """)
        
        # 2. Bảng Ga Tàu
        cursor.execute('''IF OBJECT_ID('ga_tau', 'U') IS NULL 
                          CREATE TABLE ga_tau (ma_ga NVARCHAR(50) PRIMARY KEY, ten_ga NVARCHAR(255), dia_chi NVARCHAR(MAX))''')
        
        # 3. Bảng Chuyến Tàu
        cursor.execute('''IF OBJECT_ID('chuyen_tau', 'U') IS NULL 
                          CREATE TABLE chuyen_tau (ma_chuyen NVARCHAR(50) PRIMARY KEY, ten_chuyen NVARCHAR(255), ga_di NVARCHAR(100), ga_den NVARCHAR(100), thoi_gian_di NVARCHAR(100), thoi_gian_den NVARCHAR(100))''')
        
        # 4. Bảng Khách Hàng
        cursor.execute('''IF OBJECT_ID('khach_hang', 'U') IS NULL 
                          CREATE TABLE khach_hang (cccd NVARCHAR(50) PRIMARY KEY, ho_ten NVARCHAR(255), sdt NVARCHAR(20))''')
        
        # 5. Bảng Nhân Viên
        cursor.execute('''IF OBJECT_ID('nhan_vien', 'U') IS NULL 
                          CREATE TABLE nhan_vien (ma_nv NVARCHAR(50) PRIMARY KEY, ho_ten NVARCHAR(255), chuc_vu NVARCHAR(100))''')
        
        # 6. Bảng Vé Tàu
        cursor.execute('''IF OBJECT_ID('ve_tau', 'U') IS NULL 
                          CREATE TABLE ve_tau (ma_ve NVARCHAR(50) PRIMARY KEY, ma_chuyen NVARCHAR(50), cccd_khach NVARCHAR(50), so_ghe NVARCHAR(20), gia_ve INT, ngay_mua NVARCHAR(50), ma_nv_ban NVARCHAR(50))''')

        conn.commit()
        print("Tạo các bảng trên SQL Server thành công rực rỡ!")
        
    except pyodbc.Error as e:
        print("Lỗi kết nối SQL Server:", e)
        print("Hãy chắc chắn bạn đã cài đúng ODBC Driver.")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    tao_csdl_mssql()