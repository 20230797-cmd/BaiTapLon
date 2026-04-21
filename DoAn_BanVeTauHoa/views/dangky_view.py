import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox

# Chuỗi kết nối đến SQL Server của bạn
CONN_STR = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'

class DangKyView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện bạn vừa thiết kế
        uic.loadUi('ui/DangKy.ui', self)
        self.setWindowTitle("Đăng Ký Tài Khoản Khách Hàng")
        
        # Bắt sự kiện khi bấm nút Đăng ký
        self.btn_xacnhan_dk.clicked.connect(self.thuc_hien_dang_ky)

    def thuc_hien_dang_ky(self):
        user = self.txt_taikhoan.text().strip()
        pwd = self.txt_matkhau.text().strip()
        confirm = self.txt_xacnhan.text().strip()

        # 1. Kiểm tra xem khách có để trống ô nào không
        if not user or not pwd:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ Tên tài khoản và Mật khẩu!")
            return
        
        # 2. Kiểm tra mật khẩu gõ lại có khớp không
        if pwd != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp! Vui lòng gõ lại.")
            return

        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            
            # 3. Kiểm tra xem tên đăng nhập này đã có ai xài chưa
            cursor.execute("SELECT username FROM tai_khoan WHERE username=?", (user,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "Tên tài khoản này đã có người sử dụng! Hãy chọn tên khác.")
                conn.close()
                return

            # 4. Lưu vào Database (LƯU Ý: Tự động gán quyền 'user' cho tài khoản mới)
            cursor.execute("INSERT INTO tai_khoan (username, password, vai_tro) VALUES (?, ?, 'user')", (user, pwd))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Chào mừng bạn đến với hệ thống.")
            self.close() # Tự động đóng form đăng ký sau khi xong
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Không thể kết nối CSDL: {str(e)}")