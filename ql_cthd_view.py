import pyodbc
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class DangNhapView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Đặt Vé Tàu Hỏa")
        self.setFixedSize(350, 220)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.lbl_title = QLabel("ĐĂNG NHẬP HỆ THỐNG")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: blue;")
        main_layout.addWidget(self.lbl_title)

        self.txt_taikhoan = QLineEdit()
        self.txt_taikhoan.setPlaceholderText("Nhập tên tài khoản...")
        main_layout.addWidget(self.txt_taikhoan)

        self.txt_matkhau = QLineEdit()
        self.txt_matkhau.setPlaceholderText("Nhập mật khẩu...")
        self.txt_matkhau.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.txt_matkhau)

        self.btn_dangnhap = QPushButton("Đăng Nhập")
        self.btn_dangnhap.setStyleSheet("background-color: #2ecc71; color: white; padding: 5px; font-weight: bold;")
        main_layout.addWidget(self.btn_dangnhap)

        btn_layout = QHBoxLayout()
        self.btn_dangky = QPushButton("Đăng ký mới")
        self.btn_thoat = QPushButton("Thoát")
        
        btn_layout.addWidget(self.btn_dangky)
        btn_layout.addWidget(self.btn_thoat)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Kết nối sự kiện
        self.btn_thoat.clicked.connect(self.close)
        self.btn_dangnhap.clicked.connect(self.xu_ly_dang_nhap)
        self.btn_dangky.clicked.connect(self.mo_form_dang_ky)

    def xu_ly_dang_nhap(self):
        taikhoan = self.txt_taikhoan.text().strip()
        matkhau = self.txt_matkhau.text().strip()
        
        if not taikhoan or not matkhau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT UserID, Role, FullName FROM Users WHERE Username=? AND Password=?", (taikhoan, matkhau))
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                user_id = user_data[0]
                vai_tro = user_data[1]
                ho_ten = user_data[2]
                
                # --- ĐIỂM THAY ĐỔI: Xóa chữ trong ô nhập liệu trước khi ẩn ---
                self.txt_taikhoan.clear()
                self.txt_matkhau.clear()
                self.hide() # Ẩn form đăng nhập đi
                
                # --- ĐIỂM THAY ĐỔI: Truyền chính form này (login_window=self) sang form con ---
                if vai_tro in ['Admin', 'Staff']:
                    from views.formql_view import FormQLView
                    self.form_menu = FormQLView(current_user_id=user_id, current_username=taikhoan, current_role=vai_tro, full_name=ho_ten, login_window=self)
                    self.form_menu.show()
                else:
                    from views.menu_khachhang_view import MenuKhachHangView
                    self.form_menu = MenuKhachHangView(current_user_id=user_id, username_dang_nhap=taikhoan, login_window=self)
                    self.form_menu.show()
            else:
                QMessageBox.critical(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối CSDL: {str(e)}")

    def mo_form_dang_ky(self):
        from views.dangky_view import DangKyView
        self.form_dk = DangKyView()
        self.form_dk.exec()