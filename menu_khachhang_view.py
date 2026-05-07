from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

class MenuKhachHangView(QMainWindow):
    # ĐIỂM THAY ĐỔI: Thêm login_window=None
    def __init__(self, current_user_id, username_dang_nhap, login_window=None):
        super().__init__()
        self.user_id = current_user_id
        self.username = username_dang_nhap
        self.login_window = login_window # Lưu form đăng nhập lại
        
        self.setWindowTitle(f"Hệ Thống Đặt Vé - Khách Hàng: {self.username}")
        self.setFixedSize(500, 350)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        lbl_welcome = QLabel(f"XIN CHÀO: {self.username.upper()}")
        lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_welcome.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2c3e50; 
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 5px;
        """)
        main_layout.addWidget(lbl_welcome)
        main_layout.addSpacing(20)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        self.btn_datve = self.create_button("Đặt Vé Tàu Mới", "#27ae60")   
        self.btn_lichsu = self.create_button("Lịch Sử Đặt Vé", "#2980b9")   
        self.btn_doimk = self.create_button("Đổi Mật Khẩu", "#f39c12")      
        self.btn_dangxuat = self.create_button("Đăng Xuất", "#c0392b")      

        grid_layout.addWidget(self.btn_datve, 0, 0)
        grid_layout.addWidget(self.btn_lichsu, 0, 1)
        grid_layout.addWidget(self.btn_doimk, 1, 0)
        grid_layout.addWidget(self.btn_dangxuat, 1, 1)

        main_layout.addLayout(grid_layout)

        self.btn_datve.clicked.connect(self.mo_dat_ve)
        self.btn_lichsu.clicked.connect(self.mo_lich_su)
        self.btn_doimk.clicked.connect(self.mo_doi_mat_khau)
        self.btn_dangxuat.clicked.connect(self.dang_xuat)

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setFixedSize(210, 80)
        btn.setStyleSheet(f"""
            background-color: {color}; 
            color: white; 
            font-size: 15px; 
            font-weight: bold; 
            border-radius: 8px;
        """)
        return btn

    def thong_bao_loi(self, ten_form, loi):
        QMessageBox.critical(self, "Lỗi", f"Không thể mở {ten_form}.\nChi tiết: {str(loi)}")

    # ================= CÁC HÀM ĐIỀU HƯỚNG =================

    def mo_dat_ve(self):
        try:
            from views.datve_khachhang_view import DatVeKhachHangView
            self.form_datve = DatVeKhachHangView(self.user_id, self.username)
            self.form_datve.show()
        except Exception as e:
            self.thong_bao_loi("Đặt Vé", e)

    def mo_lich_su(self):
        try:
            from views.lichsu_ve_view import LichSuVeView
            self.form_lichsu = LichSuVeView(self.user_id)
            self.form_lichsu.show()
        except Exception as e:
            self.thong_bao_loi("Lịch Sử Vé", e)

    def mo_doi_mat_khau(self):
        try:
            from views.doimatkhau_view import DoiMatKhauView
            self.form_doimk = DoiMatKhauView(self.username)
            self.form_doimk.exec()
        except Exception as e:
            self.thong_bao_loi("Đổi Mật Khẩu", e)

    # --- ĐIỂM THAY ĐỔI: Hàm xử lý Đăng xuất ---
    def dang_xuat(self):
        reply = QMessageBox.question(self, 'Xác nhận', 'Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.login_window:
                self.login_window.show() # Bật lại cửa sổ đăng nhập
            self.close() # Đóng màn hình Khách hàng lại