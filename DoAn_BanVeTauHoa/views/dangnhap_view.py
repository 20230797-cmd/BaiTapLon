import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox

# Import chuỗi kết nối
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'

# Import cả 3 form cần mở từ đây
from views.formql_view import FormQLView 
from views.menu_khachhang_view import MenuKhachHangView
from views.dangky_view import DangKyView

class DangNhapView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/DangNhap.ui', self)
        self.setWindowTitle("Đăng nhập Hệ thống")
        
        # Bắt sự kiện click chuột
        self.btn_thoat.clicked.connect(self.close)
        self.btn_dangnhap.clicked.connect(self.xu_ly_dang_nhap)
        
        # Bắt sự kiện cho nút Đăng ký mà bạn vừa thêm
        self.btn_dangky.clicked.connect(self.mo_form_dang_ky)

    def xu_ly_dang_nhap(self):
        taikhoan = self.txt_taikhoan.text().strip()
        matkhau = self.txt_matkhau.text().strip()
        
        if not taikhoan or not matkhau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        # Kiểm tra Database VÀ lấy luôn cột "vai_tro" (Quyền)
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT vai_tro FROM tai_khoan WHERE username=? AND password=?", (taikhoan, matkhau))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            vai_tro = user[0] # Lấy giá trị quyền (admin hoặc user) ra
            
            QMessageBox.information(self, "Thành công", f"Đăng nhập thành công! Quyền: {vai_tro.upper()}")
            self.hide() # Ẩn form đăng nhập
            
            # --- NGÃ BA ĐƯỜNG: PHÂN QUYỀN TRUY CẬP ---
            if vai_tro == 'admin':
                # Nếu là Admin -> Mở Menu Quản Lý 7 nút
                self.form_menu = FormQLView()
                self.form_menu.show()
            else:
                # Nếu là User -> Mở Giao diện Đặt Vé Khách Hàng
                self.form_menu = MenuKhachHangView(taikhoan)
                self.form_menu.show()
        else:
            QMessageBox.critical(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def mo_form_dang_ky(self):
        """Hàm này sẽ mở cái bảng Đăng Ký lên khi khách bấm nút"""
        self.form_dk = DangKyView()
        self.form_dk.exec()