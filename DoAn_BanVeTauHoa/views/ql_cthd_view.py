import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

CONN_STR = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'

class QLCTHDView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/QLCTHD.ui', self)
        self.setWindowTitle("Thêm Vé Vào Hóa Đơn")
        
        self.table_cthd.setColumnCount(4)
        self.table_cthd.setHorizontalHeaderLabels(["ID", "Mã HD", "Mã Vé", "Đơn Giá"])
        
        self.load_combobox()
        self.load_data()
        self.btn_them.clicked.connect(self.them_chi_tiet)

    def load_combobox(self):
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        # Lấy Mã HD
        cursor.execute("SELECT ma_hd FROM hoa_don")
        for row in cursor.fetchall():
            self.cb_hoadon.addItem(str(row[0]))
        # Lấy Vé
        cursor.execute("SELECT ma_ve, gia_ve FROM ve_tau")
        for row in cursor.fetchall():
            self.cb_ve.addItem(f"{row[0]} - Giá: {row[1]}")
        conn.close()

    def load_data(self):
        self.table_cthd.setRowCount(0)
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chi_tiet_hd")
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.table_cthd.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_cthd.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()

    def them_chi_tiet(self):
        if not self.cb_hoadon.currentText() or not self.cb_ve.currentText():
            QMessageBox.warning(self, "Lỗi", "Chưa có Hóa đơn hoặc Vé để thêm!")
            return
            
        mahd = self.cb_hoadon.currentText()
        mave = self.cb_ve.currentText().split(" - ")[0]
        dongia = self.txt_dongia.text().strip()
        if not dongia: dongia = 0
        
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chi_tiet_hd (ma_hd, ma_ve, don_gia) VALUES (?, ?, ?)", 
                           (mahd, mave, dongia))
            conn.commit()
            conn.close()
            self.load_data()
            QMessageBox.information(self, "Thành công", "Đã thêm vé này vào Hóa đơn!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))