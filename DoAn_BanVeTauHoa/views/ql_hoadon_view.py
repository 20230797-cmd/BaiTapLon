import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

# Chuỗi kết nối chuẩn của bạn
CONN_STR = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'

class QLHoaDonView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/QLHoaDon.ui', self)
        self.setWindowTitle("Quản Lý Hóa Đơn Tổng")
        
        # Cài đặt bảng 5 cột
        self.table_hoadon.setColumnCount(5)
        self.table_hoadon.setHorizontalHeaderLabels(["Mã HD", "CCCD Khách", "Mã NV", "Ngày Lập", "Tổng Tiền (VNĐ)"])
        
        self.load_combobox()
        self.load_data()
        self.btn_them.clicked.connect(self.them_hoadon)
        self.table_hoadon.cellClicked.connect(self.chon_hoadon)

    def load_combobox(self):
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        # Lấy khách hàng
        cursor.execute("SELECT cccd, ho_ten FROM khach_hang")
        for row in cursor.fetchall():
            self.cb_khachhang.addItem(f"{row[0]} - {row[1]}")
        # Lấy nhân viên
        cursor.execute("SELECT ma_nv, ho_ten FROM nhan_vien")
        for row in cursor.fetchall():
            self.cb_nhanvien.addItem(f"{row[0]} - {row[1]}")
        conn.close()

    def load_data(self):
        self.table_hoadon.setRowCount(0)
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        # Lệnh này tự động tính tổng tiền của các vé nằm trong hóa đơn
        query = """
            SELECT h.ma_hd, h.cccd_khach, h.ma_nv, h.ngay_lap, 
                   ISNULL(SUM(c.don_gia), 0) as tong_tien
            FROM hoa_don h
            LEFT JOIN chi_tiet_hd c ON h.ma_hd = c.ma_hd
            GROUP BY h.ma_hd, h.cccd_khach, h.ma_nv, h.ngay_lap
        """
        cursor.execute(query)
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.table_hoadon.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_hoadon.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()

    def them_hoadon(self):
        mahd = self.txt_mahd.text().strip()
        ngay = self.txt_ngaylap.text().strip()
        
        if not mahd:
            QMessageBox.warning(self, "Lỗi", "Nhập Mã HD!")
            return
            
        cccd = self.cb_khachhang.currentText().split(" - ")[0] if self.cb_khachhang.currentText() else ""
        manv = self.cb_nhanvien.currentText().split(" - ")[0] if self.cb_nhanvien.currentText() else ""
        
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hoa_don (ma_hd, cccd_khach, ma_nv, ngay_lap) VALUES (?, ?, ?, ?)", 
                           (mahd, cccd, manv, ngay))
            conn.commit()
            conn.close()
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã tạo Hóa Đơn Trống!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", "Mã Hóa Đơn đã tồn tại!")

    def chon_hoadon(self, row, col):
        self.txt_mahd.setText(self.table_hoadon.item(row, 0).text())