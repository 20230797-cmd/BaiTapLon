import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLKhachHangView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện Khách Hàng
        uic.loadUi('ui/QLKhachHang.ui', self)
        self.setWindowTitle("Quản Lý Khách Hàng")
        
        # Cài đặt cột cho Bảng (Chỉ có 3 cột)
        self.table_khachhang.setColumnCount(3)
        self.table_khachhang.setHorizontalHeaderLabels(["Số CCCD", "Họ và Tên", "Số Điện Thoại"])
        
        self.load_data()
        
        # Bắt sự kiện click
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_khachhang.cellClicked.connect(self.chon_dulieu)

    def load_data(self):
        self.table_khachhang.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM khach_hang").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_khachhang.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_khachhang.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Xóa trắng các ô nhập sau khi tải lại
        self.txt_cccd.clear()
        self.txt_cccd.setReadOnly(False) # Mở khóa ô CCCD
        self.txt_hoten.clear()
        self.txt_sdt.clear()

    def them_dulieu(self):
        cccd = self.txt_cccd.text().strip()
        hoten = self.txt_hoten.text().strip()
        sdt = self.txt_sdt.text().strip()

        if not cccd or not hoten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ít nhất CCCD và Họ Tên!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO khach_hang (cccd, ho_ten, sdt) VALUES (?, ?, ?)", (cccd, hoten, sdt))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm khách hàng mới!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Số CCCD này đã tồn tại trong hệ thống!")

    def chon_dulieu(self, row, col):
        self.txt_cccd.setText(self.table_khachhang.item(row, 0).text())
        self.txt_cccd.setReadOnly(True) # CCCD là khóa chính, không cho sửa
        self.txt_hoten.setText(self.table_khachhang.item(row, 1).text())
        self.txt_sdt.setText(self.table_khachhang.item(row, 2).text())

    def sua_dulieu(self):
        cccd = self.txt_cccd.text().strip()
        if not cccd:
            return
        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute("UPDATE khach_hang SET ho_ten=?, sdt=? WHERE cccd=?", 
                     (self.txt_hoten.text(), self.txt_sdt.text(), cccd))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin!")
        self.load_data()

    def xoa_dulieu(self):
        cccd = self.txt_cccd.text().strip()
        if not cccd:
            return
        reply = QMessageBox.question(self, 'Xác nhận', 'Xóa khách hàng này?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM khach_hang WHERE cccd=?", (cccd,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_khachhang.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        # Tìm theo CCCD hoặc Tên
        rows = conn.execute("SELECT * FROM khach_hang WHERE cccd LIKE ? OR ho_ten LIKE ?", (query, query)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_khachhang.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_khachhang.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()