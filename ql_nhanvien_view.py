import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QLabel)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class LichSuVeView(QDialog):
    def __init__(self, current_user_id):
        super().__init__()
        self.user_id = current_user_id
        self.setWindowTitle("Lịch Sử Đặt Vé Của Tôi")
        self.setMinimumSize(800, 400)
        
        self.init_ui()
        self.load_lich_su()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        lbl_title = QLabel("DANH SÁCH VÉ BẠN ĐÃ ĐẶT")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2980b9; margin: 10px;")
        main_layout.addWidget(lbl_title)

        self.table_lichsu = QTableWidget()
        self.table_lichsu.setColumnCount(7)
        self.table_lichsu.setHorizontalHeaderLabels([
            "Mã Vé", "Tên Hành Khách", "Mã Chuyến", "Ga Đi", "Ga Đến", "Loại Ghế", "Ngày Đặt"
        ])
        self.table_lichsu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.table_lichsu)
        self.setLayout(main_layout)

    def load_lich_su(self):
        self.table_lichsu.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # Sử dụng JOIN để lấy thông tin Ga đi, Ga đến từ bảng ChuyenTau
            # Lưu ý: Căn chỉnh lại tên bảng/cột theo đúng CSDL của bạn
            query = """
                SELECT v.MaVe, v.TenHanhKhach, v.MaChuyen, c.GaDi, c.GaDen, v.LoaiGhe, v.NgayDat
                FROM VeTau v
                LEFT JOIN ChuyenTau c ON v.MaChuyen = c.MaChuyen
                WHERE v.UserID = ?
                ORDER BY v.NgayDat DESC
            """
            cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            
            for row_idx, row_data in enumerate(rows):
                self.table_lichsu.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_lichsu.setItem(row_idx, col_idx, QTableWidgetItem(val))
                    
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải lịch sử vé: {str(e)}")