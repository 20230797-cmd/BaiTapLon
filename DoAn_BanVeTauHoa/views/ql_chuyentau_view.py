import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLChuyenTauView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện
        uic.loadUi('ui/QLChuyenTau.ui', self)
        self.setWindowTitle("Trang Quản Lý Chuyến Tàu")
        
        # Cài đặt cột cho Bảng
        self.table_chuyentau.setColumnCount(6)
        self.table_chuyentau.setHorizontalHeaderLabels(["Mã Chuyến", "Tên Chuyến", "Ga Đi", "Ga Đến", "Thời Gian Đi", "Thời Gian Đến"])
        
        # Tải dữ liệu lúc mới mở lên
        self.load_data()
        
        # Bắt sự kiện click
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_chuyentau.cellClicked.connect(self.chon_dulieu)

    def load_data(self):
        """Tải dữ liệu từ DB lên Bảng"""
        self.table_chuyentau.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM chuyen_tau").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_chuyentau.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_chuyentau.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Làm sạch form sau khi tải
        self.txt_machuyen.clear()
        self.txt_machuyen.setReadOnly(False) # Mở khóa ô nhập Mã chuyến
        self.txt_tenchuyen.clear()

    def them_dulieu(self):
        ma = self.txt_machuyen.text().strip()
        ten = self.txt_tenchuyen.text().strip()
        gadi = self.cb_gadi.currentText()
        gaden = self.cb_gaden.currentText()
        # Nếu bạn dùng QDateTimeEdit thì dùng .text(), dùng QLineEdit cũng .text()
        tgdi = self.txt_thoigiandi.text() 
        tgden = self.txt_thoigianden.text()

        if not ma or not ten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã và Tên chuyến tàu!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO chuyen_tau VALUES (?, ?, ?, ?, ?, ?)", 
                         (ma, ten, gadi, gaden, tgdi, tgden))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm chuyến tàu mới!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã chuyến tàu này đã tồn tại!")

    def chon_dulieu(self, row, col):
        """Click vào bảng thì đẩy dữ liệu lên Form"""
        self.txt_machuyen.setText(self.table_chuyentau.item(row, 0).text())
        self.txt_machuyen.setReadOnly(True) # Khóa mã chuyến, không cho sửa
        self.txt_tenchuyen.setText(self.table_chuyentau.item(row, 1).text())
        self.cb_gadi.setCurrentText(self.table_chuyentau.item(row, 2).text())
        self.cb_gaden.setCurrentText(self.table_chuyentau.item(row, 3).text())
        self.txt_thoigiandi.setText(self.table_chuyentau.item(row, 4).text())
        self.txt_thoigianden.setText(self.table_chuyentau.item(row, 5).text())

    def sua_dulieu(self):
        ma = self.txt_machuyen.text().strip()
        if not ma:
            return
        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute("UPDATE chuyen_tau SET ten_chuyen=?, ga_di=?, ga_den=?, thoi_gian_di=?, thoi_gian_den=? WHERE ma_chuyen=?", 
                     (self.txt_tenchuyen.text(), self.cb_gadi.currentText(), self.cb_gaden.currentText(), 
                      self.txt_thoigiandi.text(), self.txt_thoigianden.text(), ma))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã cập nhật chuyến tàu!")
        self.load_data()

    def xoa_dulieu(self):
        ma = self.txt_machuyen.text().strip()
        if not ma:
            return
        reply = QMessageBox.question(self, 'Xác nhận', 'Chắc chắn muốn xóa?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM chuyen_tau WHERE ma_chuyen=?", (ma,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_chuyentau.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        rows = conn.execute("SELECT * FROM chuyen_tau WHERE ma_chuyen LIKE ? OR ten_chuyen LIKE ?", (query, query)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_chuyentau.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_chuyentau.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()