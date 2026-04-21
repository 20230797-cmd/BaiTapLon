import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLNhanVienView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện Nhân Viên
        uic.loadUi('ui/QLNhanVien.ui', self)
        self.setWindowTitle("Quản Lý Nhân Viên")
        
        # Cài đặt cột cho Bảng (3 cột)
        self.table_nhanvien.setColumnCount(3)
        self.table_nhanvien.setHorizontalHeaderLabels(["Mã Nhân Viên", "Họ Tên", "Chức Vụ"])
        
        self.load_data()
        
        # Bắt sự kiện click
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_nhanvien.cellClicked.connect(self.chon_dulieu)

    def load_data(self):
        self.table_nhanvien.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM nhan_vien").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_nhanvien.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Xóa trắng form
        self.txt_manv.clear()
        self.txt_manv.setReadOnly(False) # Mở khóa ô Mã NV
        self.txt_hoten.clear()
        self.txt_chucvu.clear()

    def them_dulieu(self):
        manv = self.txt_manv.text().strip()
        hoten = self.txt_hoten.text().strip()
        chucvu = self.txt_chucvu.text().strip()

        if not manv or not hoten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã NV và Họ Tên!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO nhan_vien (ma_nv, ho_ten, chuc_vu) VALUES (?, ?, ?)", (manv, hoten, chucvu))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm nhân viên mới!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã nhân viên này đã tồn tại!")

    def chon_dulieu(self, row, col):
        """Đẩy dữ liệu từ bảng lên các ô nhập liệu"""
        self.txt_manv.setText(self.table_nhanvien.item(row, 0).text())
        self.txt_manv.setReadOnly(True) # Khóa Mã NV không cho sửa
        self.txt_hoten.setText(self.table_nhanvien.item(row, 1).text())
        self.txt_chucvu.setText(self.table_nhanvien.item(row, 2).text())

    def sua_dulieu(self):
        manv = self.txt_manv.text().strip()
        if not manv:
            return
        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute("UPDATE nhan_vien SET ho_ten=?, chuc_vu=? WHERE ma_nv=?", 
                     (self.txt_hoten.text(), self.txt_chucvu.text(), manv))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã cập nhật nhân viên!")
        self.load_data()

    def xoa_dulieu(self):
        manv = self.txt_manv.text().strip()
        if not manv:
            return
        reply = QMessageBox.question(self, 'Xác nhận', 'Chắc chắn muốn xóa Nhân viên này?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM nhan_vien WHERE ma_nv=?", (manv,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_nhanvien.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        # Tìm theo Mã NV hoặc Tên
        rows = conn.execute("SELECT * FROM nhan_vien WHERE ma_nv LIKE ? OR ho_ten LIKE ?", (query, query)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_nhanvien.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()