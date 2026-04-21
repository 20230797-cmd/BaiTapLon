import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

class QLVeView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện
        uic.loadUi('ui/QLVe.ui', self)
        self.setWindowTitle("Quản Lý Bán Vé Tàu")
        
        # Cài đặt Bảng (7 cột)
        self.table_ve.setColumnCount(7)
        self.table_ve.setHorizontalHeaderLabels(["Mã Vé", "Mã Chuyến", "CCCD Khách", "Số Ghế", "Giá Vé", "Ngày Mua", "Mã NV Bán"])
        
        # Gọi hàm tải dữ liệu
        self.load_danh_muc() # Tải data vào ComboBox trước
        self.load_data()     # Tải danh sách vé vào Bảng
        
        # Bắt sự kiện
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_ve.cellClicked.connect(self.chon_dulieu)

    def load_danh_muc(self):
        """Hàm siêu xịn: Tải dữ liệu từ các bảng khác nhét vào ComboBox"""
        conn = pyodbc.connect(CONNECTION_STRING)
        
        # 1. Tải Chuyến Tàu
        chuyen_taus = conn.execute("SELECT ma_chuyen, ten_chuyen FROM chuyen_tau").fetchall()
        self.cb_chuyentau.clear()
        for ct in chuyen_taus:
            self.cb_chuyentau.addItem(f"{ct[0]} - {ct[1]}") # Hiển thị kiểu: SE1 - Tàu Bắc Nam
            
        # 2. Tải Khách Hàng
        khach_hangs = conn.execute("SELECT cccd, ho_ten FROM khach_hang").fetchall()
        self.cb_khachhang.clear()
        for kh in khach_hangs:
            self.cb_khachhang.addItem(f"{kh[0]} - {kh[1]}")
            
        # 3. Tải Nhân Viên
        nhan_viens = conn.execute("SELECT ma_nv, ho_ten FROM nhan_vien").fetchall()
        self.cb_nhanvien.clear()
        for nv in nhan_viens:
            self.cb_nhanvien.addItem(f"{nv[0]} - {nv[1]}")
            
        conn.close()

    def load_data(self):
        self.table_ve.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        rows = conn.execute("SELECT * FROM ve_tau").fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_ve.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_ve.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()
        
        # Xóa trắng form
        self.txt_mave.clear()
        self.txt_mave.setReadOnly(False)
        self.txt_soghe.clear()
        self.txt_giave.clear()
        self.txt_ngaymua.clear()

    def get_id_from_combobox(self, text):
        """Hàm cắt chuỗi để lấy cái Mã (Nằm trước dấu gạch ngang)"""
        if not text: return ""
        return text.split(" - ")[0]

    def them_dulieu(self):
        mave = self.txt_mave.text().strip()
        machuyen = self.get_id_from_combobox(self.cb_chuyentau.currentText())
        makhach = self.get_id_from_combobox(self.cb_khachhang.currentText())
        manv = self.get_id_from_combobox(self.cb_nhanvien.currentText())
        
        soghe = self.txt_soghe.text().strip()
        giave = self.txt_giave.text().strip()
        ngaymua = self.txt_ngaymua.text().strip()

        if not mave or not machuyen or not makhach:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã Vé và chọn đầy đủ Chuyến tàu, Khách hàng!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO ve_tau VALUES (?, ?, ?, ?, ?, ?, ?)", 
                         (mave, machuyen, makhach, soghe, giave, ngaymua, manv))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã xuất vé thành công!")
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã vé này đã tồn tại!")

    def chon_dulieu(self, row, col):
        self.txt_mave.setText(self.table_ve.item(row, 0).text())
        self.txt_mave.setReadOnly(True) 
        # Vì ComboBox khó set text ngược lại chuẩn xác, ta chỉ demo đẩy dữ liệu Text Edit
        self.txt_soghe.setText(self.table_ve.item(row, 3).text())
        self.txt_giave.setText(self.table_ve.item(row, 4).text())
        self.txt_ngaymua.setText(self.table_ve.item(row, 5).text())

    def sua_dulieu(self):
        mave = self.txt_mave.text().strip()
        if not mave: return
        
        machuyen = self.get_id_from_combobox(self.cb_chuyentau.currentText())
        makhach = self.get_id_from_combobox(self.cb_khachhang.currentText())
        manv = self.get_id_from_combobox(self.cb_nhanvien.currentText())

        conn = pyodbc.connect(CONNECTION_STRING)
        conn.execute('''UPDATE ve_tau SET ma_chuyen=?, cccd_khach=?, so_ghe=?, gia_ve=?, ngay_mua=?, ma_nv_ban=? WHERE ma_ve=?''', 
                     (machuyen, makhach, self.txt_soghe.text(), self.txt_giave.text(), self.txt_ngaymua.text(), manv, mave))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Thành công", "Đã cập nhật vé!")
        self.load_data()

    def xoa_dulieu(self):
        mave = self.txt_mave.text().strip()
        if not mave: return
        reply = QMessageBox.question(self, 'Xác nhận', 'Chắc chắn muốn Hủy vé này?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM ve_tau WHERE ma_ve=?", (mave,))
            conn.commit()
            conn.close()
            self.load_data()

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.table_ve.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        query = f"%{tukhoa}%"
        rows = conn.execute("SELECT * FROM ve_tau WHERE ma_ve LIKE ? OR cccd_khach LIKE ?", (query, query)).fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table_ve.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                self.table_ve.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        conn.close()