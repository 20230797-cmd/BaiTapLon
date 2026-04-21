import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLGaTauView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện Ga Tàu
        uic.loadUi('ui/QLGaTau.ui', self)
        self.setWindowTitle("Quản Lý Ga Tàu")
        
        # Cài đặt cột cho Bảng (3 cột)
        self.table_gatau.setColumnCount(3)
        self.table_gatau.setHorizontalHeaderLabels(["Mã Ga", "Tên Ga", "Địa Chỉ"])
        
        self.load_data()
        
        # Bắt sự kiện click
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_gatau.cellClicked.connect(self.chon_dulieu)

    def load_data(self):
        self.table_gatau.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM ga_tau").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_gatau.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_gatau.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Xóa trắng form
        self.txt_maga.clear()
        self.txt_maga.setReadOnly(False) # Mở khóa ô Mã Ga
        self.txt_tenga.clear()
        self.txt_diachi.clear()

    def them_dulieu(self):
        maga = self.txt_maga.text().strip()
        tenga = self.txt_tenga.text().strip()
        diachi = self.txt_diachi.text().strip()

        if not maga or not tenga:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã ga và Tên ga!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO ga_tau (ma_ga, ten_ga, dia_chi) VALUES (?, ?, ?)", (maga, tenga, diachi))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm ga tàu mới!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã ga này đã tồn tại!")

    def chon_dulieu(self, row, col):
        """Đẩy dữ liệu từ bảng lên các ô nhập liệu"""
        self.txt_maga.setText(self.table_gatau.item(row, 0).text())
        self.txt_maga.setReadOnly(True) # Khóa Mã ga không cho sửa
        self.txt_tenga.setText(self.table_gatau.item(row, 1).text())
        self.txt_diachi.setText(self.table_gatau.item(row, 2).text())

    def sua_dulieu(self):
        maga = self.txt_maga.text().strip()
        if not maga:
            return
        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute("UPDATE ga_tau SET ten_ga=?, dia_chi=? WHERE ma_ga=?", 
                     (self.txt_tenga.text(), self.txt_diachi.text(), maga))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã cập nhật ga tàu!")
        self.load_data()

    def xoa_dulieu(self):
        maga = self.txt_maga.text().strip()
        if not maga:
            return
        reply = QMessageBox.question(self, 'Xác nhận', 'Chắc chắn muốn xóa Ga tàu này?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM ga_tau WHERE ma_ga=?", (maga,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_gatau.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        # Tìm theo Mã Ga hoặc Tên Ga
        rows = conn.execute("SELECT * FROM ga_tau WHERE ma_ga LIKE ? OR ten_ga LIKE ?", (query, query)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_gatau.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_gatau.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()