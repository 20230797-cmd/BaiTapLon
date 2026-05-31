import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLVeView(QDialog):
    def __init__(self, current_user_id=None):
        super().__init__()
        self.user_id = current_user_id # Lưu ID nhân viên thao tác nếu cần thiết
        self.setWindowTitle("Hệ Thống Quản Lý Vé Tàu")
        self.setMinimumSize(900, 500)
        
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- KHU VỰC TÌM KIẾM ---
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập mã vé, mã chuyến hoặc CCCD để tìm...")
        self.btn_tim = QPushButton("Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; padding: 6px; font-weight: bold;")
        
        search_layout.addWidget(QLabel("Tìm kiếm vé:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # --- BẢNG DỮ LIỆU ---
        self.table_ve = QTableWidget()
        self.table_ve.setColumnCount(7)
        self.table_ve.setHorizontalHeaderLabels([
            "Mã Vé", "Mã Chuyến", "ID Khách", "Tên Hành Khách", "CCCD", "Loại Ghế", "Ngày Đặt"
        ])
        self.table_ve.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_ve)

        # --- NÚT THAO TÁC ---
        btn_layout = QHBoxLayout()
        self.btn_lammoi = QPushButton("Làm Mới Danh Sách")
        self.btn_huyve = QPushButton("Hủy Vé (Xóa)")
        
        self.btn_lammoi.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px; font-weight: bold;")
        self.btn_huyve.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; font-weight: bold;")
        
        btn_layout.addStretch() # Đẩy các nút sang bên phải
        btn_layout.addWidget(self.btn_lammoi)
        btn_layout.addWidget(self.btn_huyve)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # --- KẾT NỐI SỰ KIỆN ---
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.btn_lammoi.clicked.connect(self.load_data)
        self.btn_huyve.clicked.connect(self.huy_ve)

    def load_data(self, query_filter="", params=None):
        self.table_ve.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = "SELECT MaVe, MaChuyen, UserID, TenHanhKhach, CCCD, LoaiGhe, NgayDat FROM VeTau"
            
            if query_filter:
                sql += query_filter
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_ve.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_ve.setItem(row_idx, col_idx, QTableWidgetItem(val))
            conn.close()
            self.txt_timkiem.clear()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(" WHERE MaVe LIKE ? OR MaChuyen LIKE ? OR CCCD LIKE ?", 
                       (f"%{tukhoa}%", f"%{tukhoa}%", f"%{tukhoa}%"))

    def huy_ve(self):
        # Lấy dòng đang được chọn trong bảng
        current_row = self.table_ve.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một vé trong bảng để hủy!")
            return
            
        ma_ve = self.table_ve.item(current_row, 0).text()
        ten_hk = self.table_ve.item(current_row, 3).text()
        
        reply = QMessageBox.question(self, 'Xác nhận hủy', f'Bạn có chắc chắn muốn hủy vé của hành khách: {ten_hk} (Mã vé: {ma_ve})?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                conn.execute("DELETE FROM VeTau WHERE MaVe=?", (ma_ve,))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Thành công", f"Đã hủy vé {ma_ve} thành công.")
                self.load_data() # Tải lại bảng
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể hủy vé: {str(e)}")