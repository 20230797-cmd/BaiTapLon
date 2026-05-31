import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

import sys
import os
# Đảm bảo đường dẫn import config.py của bạn là chính xác
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

# ================= CLASS 1: CỬA SỔ QUẢN LÝ LỘ TRÌNH (POP-UP) =================
class LoTrinhDialog(QDialog):
    def __init__(self, ma_chuyen):
        super().__init__()
        self.ma_chuyen = ma_chuyen
        self.setWindowTitle(f"Chi Tiết Lộ Trình - Chuyến {ma_chuyen}")
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        
        lbl_title = QLabel(f"🚩 QUẢN LÝ CÁC GA DỪNG TÀU {self.ma_chuyen}")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2980b9;")
        layout.addWidget(lbl_title)

        # Bảng hiển thị ga dừng
        self.table_lotrinh = QTableWidget()
        self.table_lotrinh.setColumnCount(6)
        self.table_lotrinh.setHorizontalHeaderLabels(["ID", "Thứ Tự", "Tên Ga", "Giờ Đến", "Giờ Đi", "Ghi Chú"])
        self.table_lotrinh.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_lotrinh.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_lotrinh.setColumnHidden(0, True) # Ẩn cột ID
        layout.addWidget(self.table_lotrinh)

        # Form thêm ga
        group_form = QGroupBox("Thêm / Cập Nhật Ga Dừng")
        form_layout = QHBoxLayout()
        
        self.txt_thutu = QLineEdit()
        self.txt_thutu.setPlaceholderText("Thứ tự (1,2,3...)")
        self.txt_thutu.setFixedWidth(80)
        
        self.txt_tenga = QLineEdit()
        self.txt_tenga.setPlaceholderText("Tên Ga")
        
        self.txt_gioden = QLineEdit()
        self.txt_gioden.setPlaceholderText("Giờ đến")
        
        self.txt_giodi = QLineEdit()
        self.txt_giodi.setPlaceholderText("Giờ đi")

        form_layout.addWidget(self.txt_thutu)
        form_layout.addWidget(self.txt_tenga)
        form_layout.addWidget(self.txt_gioden)
        form_layout.addWidget(self.txt_giodi)

        btn_them_ga = QPushButton("Lưu")
        btn_them_ga.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        btn_them_ga.clicked.connect(self.luu_ga)
        
        btn_xoa_ga = QPushButton("Xóa")
        btn_xoa_ga.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        btn_xoa_ga.clicked.connect(self.xoa_ga)

        form_layout.addWidget(btn_them_ga)
        form_layout.addWidget(btn_xoa_ga)
        group_form.setLayout(form_layout)
        
        layout.addWidget(group_form)
        self.setLayout(layout)

    # --- HÀM LOAD DATA CỦA LỘ TRÌNH (Đã được trả về nguyên bản) ---
    def load_data(self):
        self.table_lotrinh.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT ID, ThuTuDung, TenGa, ThoiGianDen, ThoiGianDi, GhiChu FROM ChiTietLoTrinh WHERE MaChuyen=? ORDER BY ThuTuDung ASC", (self.ma_chuyen,))
            for row_idx, row_data in enumerate(cursor.fetchall()):
                self.table_lotrinh.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.table_lotrinh.setItem(row_idx, col_idx, QTableWidgetItem(str(data) if data else ""))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def luu_ga(self):
        thutu = self.txt_thutu.text()
        tenga = self.txt_tenga.text()
        gioden = self.txt_gioden.text()
        giodi = self.txt_giodi.text()

        if not thutu or not tenga:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Thứ tự dừng và Tên ga!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ChiTietLoTrinh (MaChuyen, TenGa, ThuTuDung, ThoiGianDen, ThoiGianDi) 
                VALUES (?, ?, ?, ?, ?)
            """, (self.ma_chuyen, tenga, thutu, gioden, giodi))
            conn.commit()
            conn.close()
            self.load_data()
            self.txt_thutu.clear()
            self.txt_tenga.clear()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_ga(self):
        row = self.table_lotrinh.currentRow()
        if row < 0: return
        id_ga = self.table_lotrinh.item(row, 0).text()
        
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ChiTietLoTrinh WHERE ID=?", (id_ga,))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))


# ================= CLASS 2: MÀN HÌNH QUẢN LÝ CHUYẾN TÀU (CHÍNH) =================
class QLChuyenTauView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Danh Mục Chuyến Tàu & Lộ Trình")
        self.setMinimumSize(1000, 650)
        self.init_ui()
        
        # MỞ POP-UP LỘ TRÌNH KHI NHẤN ĐÚP CHUỘT VÀO 1 DÒNG TÀU
        self.table_chuyentau.itemDoubleClicked.connect(self.show_detail_info)
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập mã hoặc tên chuyến tàu cần tìm...")
        self.btn_tim = QPushButton("🔍 Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        help_label = QLabel("💡 Mẹo: Nhấn đúp chuột vào một dòng để THIẾT LẬP LỘ TRÌNH CÁC GA ĐI QUA cho chuyến tàu đó.")
        help_label.setStyleSheet("color: #d35400; font-weight: bold; font-style: italic;")
        main_layout.addWidget(help_label)

        self.table_chuyentau = QTableWidget()
        self.table_chuyentau.setColumnCount(8)
        self.table_chuyentau.setHorizontalHeaderLabels([
            "Mã Chuyến", "Tên Tàu", "Ga Đi", "Ga Đến", 
            "Ngày Đi", "Giờ Đi", "Đã Đặt", "Còn Trống"
        ])
        self.table_chuyentau.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_chuyentau.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_chuyentau.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.table_chuyentau)

        bottom_layout = QHBoxLayout()
        
        form_layout = QFormLayout()
        self.txt_machuyen = QLineEdit()
        self.txt_tenchuyen = QLineEdit()
        self.txt_gadi = QLineEdit()
        self.txt_gaden = QLineEdit()
        self.txt_ngaydi = QLineEdit()
        self.txt_giodi = QLineEdit()

        form_layout.addRow("Mã chuyến (*):", self.txt_machuyen)
        form_layout.addRow("Tên tàu (*):", self.txt_tenchuyen)
        form_layout.addRow("Ga đi (*):", self.txt_gadi)
        form_layout.addRow("Ga đến (*):", self.txt_gaden)
        form_layout.addRow("Ngày đi:", self.txt_ngaydi)
        form_layout.addRow("Giờ đi:", self.txt_giodi)
        
        bottom_layout.addLayout(form_layout, stretch=2)

        btn_layout = QVBoxLayout()
        self.btn_them = self.create_button("Thêm Mới", "#2ecc71")
        self.btn_sua = self.create_button("Cập Nhật", "#f39c12")
        self.btn_xoa = self.create_button("Xóa", "#e74c3c")
        self.btn_clear = self.create_button("Làm Mới", "#95a5a6")
        
        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)
        btn_layout.addWidget(self.btn_clear)
        
        bottom_layout.addLayout(btn_layout, stretch=1)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.btn_tim.clicked.connect(self.tim_kiem)
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_clear.clicked.connect(self.clear_form)
        self.table_chuyentau.cellClicked.connect(self.chon_dulieu)

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"background-color: {color}; color: white; padding: 8px; font-weight: bold; border-radius: 4px;")
        return btn

    def show_detail_info(self, item):
        """Mở cửa sổ quản lý lộ trình khi nhấp đúp vào chuyến tàu"""
        row = item.row()
        ma_chuyen = self.table_chuyentau.item(row, 0).text()
        
        # Gọi pop-up
        dialog = LoTrinhDialog(ma_chuyen)
        dialog.exec()

    # --- HÀM LOAD DATA CỦA CHUYẾN TÀU (Đã được cập nhật chuẩn xác) ---
    def load_data(self, query_filter="", params=None):
        self.table_chuyentau.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # Đếm chính xác từ bảng GheNgoi
            sql = """
                SELECT 
                    C.MaChuyen, C.TenChuyen, C.GaDi, C.GaDen, C.NgayDi, C.GioDi,
                    ISNULL(SUM(CASE WHEN G.TrangThai = N'Đã đặt' THEN 1 ELSE 0 END), 0) AS DaDat,
                    ISNULL(SUM(CASE WHEN G.TrangThai = N'Trống' THEN 1 ELSE 0 END), 0) AS ConTrong
                FROM ChuyenTau C
                LEFT JOIN GheNgoi G ON C.MaChuyen = G.MaChuyen
            """
            
            if query_filter:
                sql += query_filter
            
            sql += " GROUP BY C.MaChuyen, C.TenChuyen, C.GaDi, C.GaDen, C.NgayDi, C.GioDi"
                
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_chuyentau.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else "0"
                    item = QTableWidgetItem(val)
                    
                    # Đổi màu đỏ nếu số ghế trống <= 5 (sắp hết vé)
                    if col_idx == 7: 
                        if int(val) <= 5: 
                            item.setForeground(QColor("red"))
                            
                    self.table_chuyentau.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(
            query_filter=" WHERE C.MaChuyen LIKE ? OR C.TenChuyen LIKE ?", 
            params=(f"%{tukhoa}%", f"%{tukhoa}%")
        )

    def clear_form(self):
        self.txt_machuyen.clear()
        self.txt_machuyen.setReadOnly(False)
        self.txt_tenchuyen.clear()
        self.txt_gadi.clear()
        self.txt_gaden.clear()
        self.txt_ngaydi.clear()
        self.txt_giodi.clear()
        
        # Load lại bảng dữ liệu khi ấn nút Làm mới
        self.load_data()

    def chon_dulieu(self, row, col):
        self.txt_machuyen.setText(self.table_chuyentau.item(row, 0).text())
        self.txt_machuyen.setReadOnly(True)
        self.txt_tenchuyen.setText(self.table_chuyentau.item(row, 1).text())
        self.txt_gadi.setText(self.table_chuyentau.item(row, 2).text())
        self.txt_gaden.setText(self.table_chuyentau.item(row, 3).text())
        self.txt_ngaydi.setText(self.table_chuyentau.item(row, 4).text())
        self.txt_giodi.setText(self.table_chuyentau.item(row, 5).text())

    def them_dulieu(self):
        ma, ten = self.txt_machuyen.text(), self.txt_tenchuyen.text()
        di, den = self.txt_gadi.text(), self.txt_gaden.text()
        ngay, gio = self.txt_ngaydi.text(), self.txt_giodi.text()
        if not ma or not ten: return
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO ChuyenTau (MaChuyen, TenChuyen, GaDi, GaDen, NgayDi, GioDi) VALUES (?,?,?,?,?,?)", (ma, ten, di, den, ngay, gio))
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_form()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def sua_dulieu(self):
        ma = self.txt_machuyen.text()
        if not ma: return
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("UPDATE ChuyenTau SET TenChuyen=?, GaDi=?, GaDen=?, NgayDi=?, GioDi=? WHERE MaChuyen=?", 
                         (self.txt_tenchuyen.text(), self.txt_gadi.text(), self.txt_gaden.text(), 
                          self.txt_ngaydi.text(), self.txt_giodi.text(), ma))
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_form()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_dulieu(self):
        ma = self.txt_machuyen.text()
        if not ma: return
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("DELETE FROM ChuyenTau WHERE MaChuyen=?", (ma,))
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_form()
        except Exception: QMessageBox.warning(self, "Lỗi", "Không thể xóa chuyến tàu đã có dữ liệu liên quan.")

# Nếu bạn chạy trực tiếp file này (để test độc lập)
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = QLChuyenTauView()
    window.show()
    sys.exit(app.exec())