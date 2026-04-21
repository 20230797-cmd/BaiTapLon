import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLTaiKhoanView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện Tài Khoản
        uic.loadUi('ui/QLTaiKhoan.ui', self)
        self.setWindowTitle("Quản Lý Tài Khoản Đăng Nhập")
        
        # Cài đặt cột cho Bảng (2 cột)
        self.table_taikhoan.setColumnCount(2)
        self.table_taikhoan.setHorizontalHeaderLabels(["Tên Tài Khoản", "Mật Khẩu"])
        
        self.load_data()
        
        # Bắt sự kiện click
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_taikhoan.cellClicked.connect(self.chon_dulieu)

    def load_data(self):
        self.table_taikhoan.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM tai_khoan").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_taikhoan.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Xóa trắng form
        self.txt_taikhoan.clear()
        self.txt_taikhoan.setReadOnly(False) # Mở khóa ô Tài khoản
        self.txt_matkhau.clear()

    def them_dulieu(self):
        taikhoan = self.txt_taikhoan.text().strip()
        matkhau = self.txt_matkhau.text().strip()

        if not taikhoan or not matkhau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ Tài khoản và Mật khẩu!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO tai_khoan (username, password) VALUES (?, ?)", (taikhoan, matkhau))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã cấp tài khoản mới!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Tên tài khoản này đã tồn tại!")

    def chon_dulieu(self, row, col):
        """Đẩy dữ liệu từ bảng lên các ô nhập liệu"""
        self.txt_taikhoan.setText(self.table_taikhoan.item(row, 0).text())
        self.txt_taikhoan.setReadOnly(True) # Khóa tên tài khoản không cho sửa
        self.txt_matkhau.setText(self.table_taikhoan.item(row, 1).text())

    def sua_dulieu(self):
        taikhoan = self.txt_taikhoan.text().strip()
        if not taikhoan:
            return
        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute("UPDATE tai_khoan SET password=? WHERE username=?", 
                     (self.txt_matkhau.text(), taikhoan))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã đổi mật khẩu!")
        self.load_data()

    def xoa_dulieu(self):
        taikhoan = self.txt_taikhoan.text().strip()
        if not taikhoan:
            return
            
        if taikhoan.lower() == 'admin':
            QMessageBox.critical(self, "Cảnh báo", "Không được phép xóa tài khoản Admin gốc!")
            return
            
        reply = QMessageBox.question(self, 'Xác nhận', 'Chắc chắn muốn thu hồi tài khoản này?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM tai_khoan WHERE username=?", (taikhoan,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_taikhoan.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        rows = conn.execute("SELECT * FROM tai_khoan WHERE username LIKE ?", (query,)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_taikhoan.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()