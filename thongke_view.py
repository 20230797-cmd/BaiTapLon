import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QPushButton)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class ThongKeView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo Cáo Thống Kê Bán Vé")
        self.setMinimumSize(700, 400)
        self.init_ui()
        self.load_thong_ke()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Tiêu đề
        lbl_title = QLabel("THỐNG KÊ SỐ LƯỢNG VÉ ĐÃ BÁN THEO CHUYẾN TÀU")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #8e44ad; margin-bottom: 15px;")
        main_layout.addWidget(lbl_title)

        # Bảng thống kê
        self.table_thongke = QTableWidget()
        self.table_thongke.setColumnCount(3)
        self.table_thongke.setHorizontalHeaderLabels(["Mã Chuyến Tàu", "Tên Chuyến Tàu", "Tổng Số Vé Đã Bán"])
        self.table_thongke.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.table_thongke)

        # Nút Làm mới
        self.btn_lammoi = QPushButton("Cập Nhật Dữ Liệu Tức Thời")
        self.btn_lammoi.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; font-weight: bold;")
        self.btn_lammoi.clicked.connect(self.load_thong_ke)
        main_layout.addWidget(self.btn_lammoi)

        self.setLayout(main_layout)

    def load_thong_ke(self):
        self.table_thongke.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # Câu lệnh SQL gom nhóm đếm số vé theo mã chuyến
            query = """
                SELECT c.MaChuyen, c.TenChuyen, COUNT(v.MaVe) as SoVeDaBan
                FROM ChuyenTau c
                LEFT JOIN VeTau v ON c.MaChuyen = v.MaChuyen
                GROUP BY c.MaChuyen, c.TenChuyen
                ORDER BY SoVeDaBan DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row_idx, row_data in enumerate(rows):
                self.table_thongke.insertRow(row_idx)
                # Cột 1: Mã chuyến
                self.table_thongke.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
                # Cột 2: Tên chuyến
                self.table_thongke.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
                
                # Cột 3: Số vé đã bán (Căn giữa và tô màu cho đẹp)
                item_sove = QTableWidgetItem(str(row_data[2]))
                item_sove.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if row_data[2] > 0:
                    item_sove.setBackground(Qt.GlobalColor.green) # Tô xanh nếu có bán được vé
                    item_sove.setForeground(Qt.GlobalColor.white)
                self.table_thongke.setItem(row_idx, 2, item_sove)
                
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Thống Kê", f"Lỗi truy vấn dữ liệu: {str(e)}")