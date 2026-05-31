from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

class FormQLView(QDialog):
    def __init__(self, current_user_id, current_username, current_role="Staff", full_name="Người dùng", login_window=None):
        super().__init__()
        self.user_id = current_user_id
        self.username = current_username
        self.role = current_role
        self.login_window = login_window 
        
        self.setWindowTitle(f"Phần mềm Quản Lý & Bán Vé - [{self.role}] {full_name}")
        self.setFixedSize(650, 550) # Tăng chiều cao lên 550 để chứa thêm hàng
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
        
        # ================= TẠO CÁC NÚT BẤM =================
        self.btn_banve_quay = self.create_menu_button("BÁN VÉ\nTẠI QUẦY", "#27ae60") 
        self.btn_ql_chuyentau = self.create_menu_button("Quản Lý\nChuyến Tàu", "#3498db")
        self.btn_ql_gatau = self.create_menu_button("Quản Lý\nGa Tàu", "#9b59b6")
        
        self.btn_ql_ve = self.create_menu_button("Quản Lý\nVé Tàu", "#1abc9c")
        self.btn_ql_khachhang = self.create_menu_button("Quản Lý\nKhách Hàng", "#3498db")
        self.btn_ql_nhanvien = self.create_menu_button("Quản Lý\nNhân Viên", "#e67e22")
        
        self.btn_ql_taikhoan = self.create_menu_button("Quản Lý\nTài Khoản", "#e74c3c")
        self.btn_thongke = self.create_menu_button("Thống Kê\nKPI", "#f1c40f")
        self.btn_thongke.setStyleSheet("background-color: #f1c40f; color: black; font-size: 14px; font-weight: bold; border-radius: 8px;")
        
        # ĐIỂM THAY ĐỔI: Thêm nút Sức chứa
        self.btn_succhua = self.create_menu_button("Sức Chứa\nKhoang Tàu", "#8e44ad")
        
        # Nút đăng xuất làm riêng cho nổi bật
        self.btn_dangxuat = QPushButton("ĐĂNG XUẤT")
        self.btn_dangxuat.setFixedHeight(50)
        self.btn_dangxuat.setStyleSheet("background-color: #c0392b; color: white; font-size: 14px; font-weight: bold; border-radius: 8px;")

        # ================= SẮP XẾP VÀO LƯỚI =================
        grid_layout.addWidget(self.btn_banve_quay, 0, 0)
        grid_layout.addWidget(self.btn_ql_chuyentau, 0, 1)
        grid_layout.addWidget(self.btn_ql_gatau, 0, 2)
        
        grid_layout.addWidget(self.btn_ql_ve, 1, 0)
        grid_layout.addWidget(self.btn_ql_khachhang, 1, 1)
        grid_layout.addWidget(self.btn_ql_nhanvien, 1, 2)
        
        grid_layout.addWidget(self.btn_ql_taikhoan, 2, 0)
        grid_layout.addWidget(self.btn_thongke, 2, 1) 
        grid_layout.addWidget(self.btn_succhua, 2, 2) # Nút sức chứa thay vào chỗ Đăng xuất cũ

        main_layout.addLayout(grid_layout)
        
        # Thêm nút đăng xuất xuống dưới cùng
        main_layout.addSpacing(10)
        main_layout.addWidget(self.btn_dangxuat)
        
        self.setLayout(main_layout)

        # ================= XỬ LÝ PHÂN QUYỀN CHẶT CHẼ =================
        if self.role == 'Admin':
            self.btn_banve_quay.hide()
        elif self.role == 'Staff':
            self.btn_ql_nhanvien.hide()
            self.btn_ql_taikhoan.hide()
            self.btn_thongke.hide()
            # Nút sức chứa vẫn hiện cho Staff dùng bình thường

        # ================= KẾT NỐI SỰ KIỆN =================
        self.btn_banve_quay.clicked.connect(self.mo_banve_quay)
        self.btn_ql_chuyentau.clicked.connect(self.mo_ql_chuyentau)
        self.btn_ql_gatau.clicked.connect(self.mo_ql_gatau)
        self.btn_ql_khachhang.clicked.connect(self.mo_ql_khachhang)
        self.btn_ql_ve.clicked.connect(self.mo_ql_ve)
        self.btn_ql_nhanvien.clicked.connect(self.mo_ql_nhanvien)
        self.btn_ql_taikhoan.clicked.connect(self.mo_ql_taikhoan)
        self.btn_thongke.clicked.connect(self.mo_thongke)
        self.btn_succhua.clicked.connect(self.mo_succhua) # Kết nối sự kiện Sức chứa
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
                self.login_window.show() 
            self.close() 

    # --- CÁC HÀM MỞ FORM ---
    def mo_banve_quay(self):
        try:
            from views.banve_quay_view import BanVeQuayView
            self.form_bv = BanVeQuayView(self.user_id, self.username)
            self.form_bv.exec()
        except Exception as e:
            self.thong_bao_loi("Bán Vé Tại Quầy", e)

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
            
    # ĐIỂM THAY ĐỔI: Hàm mở form Sức Chứa
    def mo_succhua(self):
        try:
            from views.suc_chua_view import SucChuaView
            self.form_succhua = SucChuaView()
            self.form_succhua.exec()
        except Exception as e:
            self.thong_bao_loi("Sức Chứa Khoang Tàu", e)