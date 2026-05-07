import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLChuyenTauView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Danh Mục Chuyến Tàu & Tư Vấn Lộ Trình")
        self.setMinimumSize(1000, 650)
        
        self.init_ui()
        
        # KẾT NỐI SỰ KIỆN NHẤN ĐÚP ĐỂ XEM CHI TIẾT
        self.table_chuyentau.itemDoubleClicked.connect(self.show_detail_info)
        
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ================= 1. KHU VỰC TÌM KIẾM =================
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập mã hoặc tên chuyến tàu cần tìm...")
        self.btn_tim = QPushButton("🔍 Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # Hướng dẫn nhỏ cho nhân viên
        help_label = QLabel("💡 Mẹo: Nhấn đúp vào một dòng để xem chi tiết lộ trình tư vấn cho khách.")
        help_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        main_layout.addWidget(help_label)

        # ================= 2. KHU VỰC BẢNG DỮ LIỆU =================
        self.table_chuyentau = QTableWidget()
        self.table_chuyentau.setColumnCount(8)
        self.table_chuyentau.setHorizontalHeaderLabels([
            "Mã Chuyến", "Tên Tàu", "Ga Đi", "Ga Đến", 
            "Ngày Đi", "Giờ Đi", "Đã Đặt", "Còn Trống"
        ])
        
        # Cấu hình bảng chuyên nghiệp hơn
        self.table_chuyentau.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_chuyentau.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_chuyentau.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        main_layout.addWidget(self.table_chuyentau)

        # ================= 3. KHU VỰC NHẬP LIỆU & NÚT BẤM =================
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

        # KẾT NỐI SỰ KIỆN
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
        """Hàm hiện cửa sổ tư vấn lộ trình chi tiết lấy từ cột LoTrinh"""
        row = item.row()
        ma_chuyen = self.table_chuyentau.item(row, 0).text()
        
        try:
            # Truy vấn lấy lộ trình chi tiết từ DB
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT TenChuyen, GaDi, GaDen, LoTrinh FROM ChuyenTau WHERE MaChuyen = ?", (ma_chuyen,))
            res = cursor.fetchone()
            conn.close()

            if res:
                ten_tau, gadi, gaden, lotrinh = res
                # Nếu lộ trình trống thì báo chưa cập nhật
                lotrinh_hien_thi = lotrinh if lotrinh else "Chưa cập nhật lộ trình chi tiết."

                msg = f"--- THÔNG TIN LỘ TRÌNH CHI TIẾT ---\n\n"
                msg += f"Tàu: {ten_tau} ({ma_chuyen})\n"
                msg += f"Tuyến chính: {gadi} ➔ {gaden}\n\n"
                msg += f"🚩 CÁC GA ĐI QUA:\n{lotrinh_hien_thi}\n\n"
                msg += f"💡 Ghi chú: Nhân viên nhắc khách có mặt trước 30p."
                
                QMessageBox.information(self, f"Tư vấn lộ trình {ma_chuyen}", msg)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lấy lộ trình: {str(e)}")

    def load_data(self, query_filter="", params=None):
        self.table_chuyentau.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    C.MaChuyen, C.TenChuyen, C.GaDi, C.GaDen, C.NgayDi, C.GioDi,
                    COUNT(V.MaVe) as DaDat,
                    (100 - COUNT(V.MaVe)) as ConTrong
                FROM ChuyenTau C
                LEFT JOIN VeTau V ON C.MaChuyen = V.MaChuyen
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
                    if col_idx == 7: # Cột Còn Trống
                        if int(val) <= 5: 
                            item.setForeground(QColor("red"))
                    self.table_chuyentau.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        # SỬA LỖI TRONG NÀY: Thêm C. để phân biệt cột
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
            conn.execute("INSERT INTO ChuyenTau VALUES (?,?,?,?,?,?)", (ma, ten, di, den, ngay, gio))
            conn.commit()
            conn.close()
            self.load_data()
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
        except Exception: QMessageBox.warning(self, "Lỗi", "Không thể xóa chuyến tàu đã có vé đặt.")