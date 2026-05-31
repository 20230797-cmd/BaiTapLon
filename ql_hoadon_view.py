import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class DoiMatKhauView(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username # Nhận tên tài khoản từ Menu truyền sang
        self.setWindowTitle("Đổi Mật Khẩu")
        self.setFixedSize(350, 220)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Tiêu đề
        lbl_title = QLabel(f"ĐỔI MẬT KHẨU TÀI KHOẢN: {self.username}")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-weight: bold; color: #d35400; font-size: 14px;")
        main_layout.addWidget(lbl_title)
        main_layout.addSpacing(10)

        # Form nhập liệu
        form_layout = QFormLayout()
        self.txt_mk_cu = QLineEdit()
        self.txt_mk_cu.setEchoMode(QLineEdit.EchoMode.Password) # Ẩn text thành dấu chấm
        self.txt_mk_moi = QLineEdit()
        self.txt_mk_moi.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_xacnhan = QLineEdit()
        self.txt_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Mật khẩu cũ:", self.txt_mk_cu)
        form_layout.addRow("Mật khẩu mới:", self.txt_mk_moi)
        form_layout.addRow("Xác nhận MK:", self.txt_xacnhan)
        main_layout.addLayout(form_layout)

        # Cụm Nút bấm
        btn_layout = QHBoxLayout()
        self.btn_luu = QPushButton("Lưu Thay Đổi")
        self.btn_luu.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 5px;")
        self.btn_huy = QPushButton("Hủy")
        
        btn_layout.addWidget(self.btn_luu)
        btn_layout.addWidget(self.btn_huy)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Kết nối sự kiện
        self.btn_luu.clicked.connect(self.thuc_hien_doi_mk)
        self.btn_huy.clicked.connect(self.reject) # Lệnh đóng Dialog

    def thuc_hien_doi_mk(self):
        mk_cu = self.txt_mk_cu.text().strip()
        mk_moi = self.txt_mk_moi.text().strip()
        xacnhan = self.txt_xacnhan.text().strip()

        # 1. Kiểm tra trống
        if not mk_cu or not mk_moi or not xacnhan:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # 2. Kiểm tra khớp mật khẩu
        if mk_moi != xacnhan:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # 3. Kiểm tra mật khẩu cũ trong Database có đúng không
            cursor.execute("SELECT Password FROM Users WHERE Username=?", (self.username,))
            row = cursor.fetchone()
            
            if not row or row[0] != mk_cu:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu cũ không chính xác!")
                conn.close()
                return

            # 4. Nếu đúng thì tiến hành Update mật khẩu mới
            cursor.execute("UPDATE Users SET Password=? WHERE Username=?", (mk_moi, self.username))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công!")
            self.accept() # Đóng form và trả về kết quả thành công
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))