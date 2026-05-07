import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QComboBox)
from PyQt6.QtCore import Qt
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class DatVeKhachHangView(QDialog):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.setWindowTitle(f"Đặt Vé Tàu Mới - Khách hàng: {self.username}")
        self.setMinimumSize(850, 650)
        
        self.init_ui()
        self.load_chuyen_tau() # Tải danh sách chuyến tàu lên bảng

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ================= 1. KHU VỰC TÌM KIẾM CHUYẾN TÀU =================
        search_layout = QHBoxLayout()
        self.txt_gadi = QLineEdit()
        self.txt_gadi.setPlaceholderText("Ga đi...")
        self.txt_gaden = QLineEdit()
        self.txt_gaden.setPlaceholderText("Ga đến...")
        
        self.btn_tim = QPushButton("Tìm Chuyến Tàu")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; padding: 5px; font-weight: bold;")
        
        search_layout.addWidget(QLabel("Từ:"))
        search_layout.addWidget(self.txt_gadi)
        search_layout.addWidget(QLabel("Đến:"))
        search_layout.addWidget(self.txt_gaden)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # ================= 2. BẢNG DANH SÁCH CHUYẾN TÀU =================
        self.table_chuyen = QTableWidget()
        self.table_chuyen.setColumnCount(6)
        self.table_chuyen.setHorizontalHeaderLabels(["Mã Chuyến", "Tên Chuyến", "Ga Đi", "Ga Đến", "Ngày Đi", "Giờ"])
        self.table_chuyen.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_chuyen)

        # ================= 3. KHU VỰC THÔNG TIN ĐẶT VÉ =================
        lbl_info = QLabel("THÔNG TIN ĐẶT VÉ")
        lbl_info.setStyleSheet("font-weight: bold; color: #d35400; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(lbl_info)

        bottom_layout = QHBoxLayout()
        form_layout = QFormLayout()
        
        # Các ô thông tin
        self.txt_machuyen = QLineEdit()
        self.txt_machuyen.setPlaceholderText("Chọn một chuyến tàu từ bảng ở trên...")
        self.txt_machuyen.setReadOnly(True) # Khóa, chỉ cho phép chọn từ bảng
        
        self.txt_ten = QLineEdit(self.username) # Gợi ý tên bằng username
        self.txt_cccd = QLineEdit()
        self.cb_loaighe = QComboBox()
        self.cb_loaighe.addItems(["Ngồi Cứng (250k)", "Ngồi Mềm Điều Hòa (350k)", "Giường Nằm (550k)"])

        form_layout.addRow("Mã Chuyến (*):", self.txt_machuyen)
        form_layout.addRow("Tên Hành Khách (*):", self.txt_ten)
        form_layout.addRow("CCCD/CMND (*):", self.txt_cccd)
        form_layout.addRow("Loại Ghế:", self.cb_loaighe)
        bottom_layout.addLayout(form_layout, stretch=2)

        # Nút Đặt Vé
        btn_layout = QVBoxLayout()
        self.btn_datve = QPushButton("XÁC NHẬN ĐẶT VÉ")
        self.btn_datve.setFixedSize(200, 60)
        self.btn_datve.setStyleSheet("background-color: #27ae60; color: white; font-size: 14px; font-weight: bold; border-radius: 8px;")
        btn_layout.addWidget(self.btn_datve)
        bottom_layout.addLayout(btn_layout, stretch=1)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        # ================= KẾT NỐI SỰ KIỆN =================
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.table_chuyen.cellClicked.connect(self.chon_chuyen_tau)
        self.btn_datve.clicked.connect(self.thuc_hien_dat_ve)

    def load_chuyen_tau(self, query_filter="", params=None):
        self.table_chuyen.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = "SELECT MaChuyen, TenChuyen, GaDi, GaDen, NgayDi, GioDi FROM ChuyenTau"
            
            if query_filter:
                sql += query_filter
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_chuyen.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_chuyen.setItem(row_idx, col_idx, QTableWidgetItem(val))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def tim_kiem(self):
        gadi = self.txt_gadi.text().strip()
        gaden = self.txt_gaden.text().strip()
        self.load_chuyen_tau(" WHERE GaDi LIKE ? AND GaDen LIKE ?", (f"%{gadi}%", f"%{gaden}%"))

    def chon_chuyen_tau(self, row, col):
        """Lấy mã chuyến tàu từ dòng được click đẩy xuống form Đặt vé"""
        ma_chuyen = self.table_chuyen.item(row, 0).text()
        self.txt_machuyen.setText(ma_chuyen)

    def thuc_hien_dat_ve(self):
        ma_chuyen = self.txt_machuyen.text().strip()
        ten_hk = self.txt_ten.text().strip()
        cccd = self.txt_cccd.text().strip()
        loai_ghe = self.cb_loaighe.currentText()
        ngay_dat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not ma_chuyen:
            QMessageBox.warning(self, "Lỗi", "Vui lòng click chọn một chuyến tàu từ danh sách ở trên!")
            return
        if not ten_hk or not cccd:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên hành khách và CCCD!")
            return

        # Xác nhận lần cuối
        reply = QMessageBox.question(self, 'Xác nhận', f'Bạn muốn đặt vé cho chuyến {ma_chuyen}?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                # Câu lệnh INSERT (Điều chỉnh tên bảng/cột cho khớp với Database của bạn)
                query = "INSERT INTO VeTau (MaChuyen, UserID, TenHanhKhach, CCCD, LoaiGhe, NgayDat) VALUES (?, ?, ?, ?, ?, ?)"
                conn.execute(query, (ma_chuyen, self.user_id, ten_hk, cccd, loai_ghe, ngay_dat))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Thành công", "Chúc mừng! Bạn đã đặt vé thành công.")
                self.close() # Đặt xong thì đóng form
            except Exception as e:
                QMessageBox.critical(self, "Lỗi Database", str(e))