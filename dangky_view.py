import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class DangKyView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng Ký Tài Khoản Khách Hàng")
        self.setFixedSize(350, 300)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Tiêu đề
        lbl_title = QLabel("TẠO TÀI KHOẢN MỚI")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e67e22; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)

        # Form nhập liệu
        form_layout = QFormLayout()
        
        self.txt_taikhoan = QLineEdit()
        self.txt_matkhau = QLineEdit()
        self.txt_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_xacnhan = QLineEdit()
        self.txt_xacnhan.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_hoten = QLineEdit()
        self.txt_sdt = QLineEdit()

        form_layout.addRow("Tên tài khoản (*):", self.txt_taikhoan)
        form_layout.addRow("Mật khẩu (*):", self.txt_matkhau)
        form_layout.addRow("Xác nhận MK (*):", self.txt_xacnhan)
        form_layout.addRow("Họ và tên (*):", self.txt_hoten)
        form_layout.addRow("Số điện thoại:", self.txt_sdt)
        
        main_layout.addLayout(form_layout)

        # Nút bấm
        btn_layout = QHBoxLayout()
        self.btn_xacnhan_dk = QPushButton("Đăng Ký")
        self.btn_xacnhan_dk.setStyleSheet("background-color: #27ae60; color: white; padding: 5px; font-weight: bold;")
        self.btn_huy = QPushButton("Hủy")
        
        btn_layout.addWidget(self.btn_xacnhan_dk)
        btn_layout.addWidget(self.btn_huy)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Bắt sự kiện
        self.btn_xacnhan_dk.clicked.connect(self.thuc_hien_dang_ky)
        self.btn_huy.clicked.connect(self.reject) # Đóng form đăng ký

    def thuc_hien_dang_ky(self):
        user = self.txt_taikhoan.text().strip()
        pwd = self.txt_matkhau.text().strip()
        confirm = self.txt_xacnhan.text().strip()
        hoten = self.txt_hoten.text().strip()
        sdt = self.txt_sdt.text().strip()

        if not user or not pwd or not hoten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ các trường có dấu (*)!")
            return
        
        if pwd != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            cursor.execute("SELECT Username FROM Users WHERE Username=?", (user,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "Tài khoản này đã tồn tại!")
                conn.close()
                return

            # Insert với Role mặc định là 'User'
            query = """
                INSERT INTO Users (Username, Password, FullName, Phone, Role, CreatedBy) 
                VALUES (?, ?, ?, ?, 'User', NULL)
            """
            cursor.execute(query, (user, pwd, hoten, sdt))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi hệ thống: {str(e)}")