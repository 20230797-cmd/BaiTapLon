from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

class FormQLView(QDialog):
    # ĐIỂM THAY ĐỔI: Nhận thêm biến login_window
    def __init__(self, current_user_id, current_username, current_role="Staff", full_name="Người dùng", login_window=None):
        super().__init__()
        self.user_id = current_user_id
        self.username = current_username
        self.role = current_role
        self.login_window = login_window # Lưu màn hình đăng nhập lại
        
        self.setWindowTitle(f"Phần mềm Bán Vé Tại Quầy - [{self.role}] {full_name}")
        self.setFixedSize(650, 400)
        self.init_ui(full_name)

    def init_ui(self, full_name):
        main_layout = QVBoxLayout()

        lbl_info = QLabel(f"Xin chào: {full_name} | Quyền truy cập: {self.role}")
        lbl_info.setStyleSheet("background-color: #34495e; color: white; padding: 15px; font-size: 15px; font-weight: bold;")
        lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_info)
        main_layout.addSpacing(10)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15) 
        
        self.btn_ql_chuyentau = self.create_menu_button("Quản Lý\nChuyến Tàu", "#3498db")
        self.btn_ql_gatau = self.create_menu_button("Quản Lý\nGa Tàu", "#9b59b6")
        self.btn_ql_ve = self.create_menu_button("Quản Lý\nVé Tàu", "#1abc9c")
        
        self.btn_ql_khachhang = self.create_menu_button("Quản Lý\nKhách Hàng", "#3498db")
        self.btn_ql_nhanvien = self.create_menu_button("Quản Lý\nNhân Viên", "#e67e22")
        self.btn_ql_taikhoan = self.create_menu_button("Quản Lý\nTài Khoản", "#e74c3c")
        
        self.btn_thongke = self.create_menu_button("Thống Kê\nDoanh Thu", "#f1c40f")
        self.btn_thongke.setStyleSheet("background-color: #f1c40f; color: black; font-size: 14px; font-weight: bold; border-radius: 8px;")

        # ĐIỂM THAY ĐỔI: Thêm nút Đăng Xuất màu đỏ sẫm
        self.btn_dangxuat = self.create_menu_button("Đăng Xuất", "#c0392b")

        grid_layout.addWidget(self.btn_ql_chuyentau, 0, 0)
        grid_layout.addWidget(self.btn_ql_gatau, 0, 1)
        grid_layout.addWidget(self.btn_ql_ve, 0, 2)
        
        grid_layout.addWidget(self.btn_ql_khachhang, 1, 0)
        grid_layout.addWidget(self.btn_ql_nhanvien, 1, 1)
        grid_layout.addWidget(self.btn_ql_taikhoan, 1, 2)
        
        grid_layout.addWidget(self.btn_thongke, 2, 1) 
        grid_layout.addWidget(self.btn_dangxuat, 2, 2) # Xếp vào cột 3 hàng 3

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        if self.role == 'Staff':
            self.btn_ql_nhanvien.hide()
            self.btn_ql_taikhoan.hide()
            self.btn_thongke.hide()

        self.btn_ql_chuyentau.clicked.connect(self.mo_ql_chuyentau)
        self.btn_ql_gatau.clicked.connect(self.mo_ql_gatau)
        self.btn_ql_khachhang.clicked.connect(self.mo_ql_khachhang)
        self.btn_ql_ve.clicked.connect(self.mo_ql_ve)
        self.btn_ql_nhanvien.clicked.connect(self.mo_ql_nhanvien)
        self.btn_ql_taikhoan.clicked.connect(self.mo_ql_taikhoan)
        self.btn_thongke.clicked.connect(self.mo_thongke)
        
        # ĐIỂM THAY ĐỔI: Kết nối sự kiện đăng xuất
        self.btn_dangxuat.clicked.connect(self.dang_xuat)

    def create_menu_button(self, text, color):
        btn = QPushButton(text)
        btn.setFixedSize(180, 90)
        btn.setStyleSheet(f"background-color: {color}; color: white; font-size: 14px; font-weight: bold; border-radius: 8px;")
        return btn

    def thong_bao_loi(self, ten_form, loi):
        QMessageBox.critical(self, "Lỗi Tải Form", f"Không thể mở {ten_form}.\nChi tiết lỗi: {str(loi)}")

    # --- HÀM XỬ LÝ ĐĂNG XUẤT ---
    def dang_xuat(self):
        reply = QMessageBox.question(self, 'Xác nhận', 'Bạn có chắc chắn muốn đăng xuất?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.login_window:
                self.login_window.show() # Hiện lại form Đăng Nhập
            self.close() # Đóng form Quản Lý đi

    # --- CÁC HÀM MỞ FORM (Giữ nguyên) ---
    def mo_ql_chuyentau(self):
        try:
            from views.ql_chuyentau_view import QLChuyenTauView
            self.form_chuyentau = QLChuyenTauView() 
            self.form_chuyentau.exec()
        except Exception as e:
            self.thong_bao_loi("QL Chuyến Tàu", e)

    def mo_ql_gatau(self):
        try:
            from views.ql_gatau_view import QLGaTauView
            self.form_gatau = QLGaTauView()
            self.form_gatau.exec()
        except Exception as e:
            self.thong_bao_loi("QL Ga Tàu", e)

    def mo_ql_khachhang(self):
        try:
            from views.ql_khachhang_view import QLKhachHangView
            self.form_khachhang = QLKhachHangView()
            self.form_khachhang.exec()
        except Exception as e:
            self.thong_bao_loi("QL Khách Hàng", e)

    def mo_ql_ve(self):
        try:
            from views.ql_ve_view import QLVeView
            self.form_ve = QLVeView(current_user_id=self.user_id)
            self.form_ve.exec()
        except Exception as e:
            self.thong_bao_loi("QL Vé Tàu", e)

    def mo_ql_nhanvien(self):
        try:
            from views.ql_nhanvien_view import QLNhanVienView
            self.form_nhanvien = QLNhanVienView()
            self.form_nhanvien.exec()
        except Exception as e:
            self.thong_bao_loi("QL Nhân Viên", e)

    def mo_ql_taikhoan(self):
        try:
            from views.ql_taikhoan_view import QLTaiKhoanView
            self.form_taikhoan = QLTaiKhoanView(current_admin_id=self.user_id)
            self.form_taikhoan.exec()
        except Exception as e:
            self.thong_bao_loi("QL Tài Khoản", e)

    def mo_thongke(self):
        try:
            from views.thongke_view import ThongKeView
            self.form_thongke = ThongKeView()
            self.form_thongke.exec()
        except Exception as e:
            self.thong_bao_loi("Thống Kê", e)