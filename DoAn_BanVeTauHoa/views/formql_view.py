from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox

# Khai báo các form bạn đã làm xong
from views.ql_chuyentau_view import QLChuyenTauView
from views.ql_khachhang_view import QLKhachHangView

class FormQLView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Load file giao diện (giờ chỉ còn 7 nút)
        uic.loadUi('ui/FormQL.ui', self)
        self.setWindowTitle("Menu Quản Lý Trung Tâm (Admin)")
        
        # Kết nối sự kiện Click cho 7 nút
        self.btn_ql_chuyentau.clicked.connect(self.mo_ql_chuyentau)
        self.btn_ql_khachhang.clicked.connect(self.mo_ql_khachhang)
        self.btn_ql_taikhoan.clicked.connect(self.mo_ql_taikhoan)
        self.btn_ql_gatau.clicked.connect(self.mo_ql_gatau)
        self.btn_ql_ve.clicked.connect(self.mo_ql_ve)
        self.btn_ql_nhanvien.clicked.connect(self.mo_ql_nhanvien)
        self.btn_thongke.clicked.connect(self.mo_thongke)

    def thong_bao_tam(self, ten_form):
        QMessageBox.information(self, "Thông báo", f"Form {ten_form} chưa được tạo file code.")

    # ---------------- CÁC HÀM MỞ FORM CHI TIẾT ----------------

    def mo_ql_chuyentau(self):
        self.form_chuyentau = QLChuyenTauView()
        self.form_chuyentau.exec()

    def mo_ql_khachhang(self):
        self.form_khachhang = QLKhachHangView()
        self.form_khachhang.exec()

    def mo_ql_taikhoan(self):
        try:
            from views.ql_taikhoan_view import QLTaiKhoanView
            self.form_taikhoan = QLTaiKhoanView()
            self.form_taikhoan.exec()
        except ImportError:
            self.thong_bao_tam("QL Tài Khoản")

    def mo_ql_gatau(self):
        try:
            from views.ql_gatau_view import QLGaTauView
            self.form_gatau = QLGaTauView()
            self.form_gatau.exec()
        except ImportError:
            self.thong_bao_tam("QL Ga Tàu")

    def mo_ql_ve(self):
        try:
            from views.ql_ve_view import QLVeView
            self.form_ve = QLVeView()
            self.form_ve.exec()
        except ImportError:
            self.thong_bao_tam("QL Vé Tàu")

    def mo_ql_nhanvien(self):
        try:
            from views.ql_nhanvien_view import QLNhanVienView
            self.form_nhanvien = QLNhanVienView()
            self.form_nhanvien.exec()
        except ImportError:
            self.thong_bao_tam("QL Nhân Viên")

    def mo_thongke(self):
        try:
            from views.thongke_view import ThongKeView
            self.form_thongke = ThongKeView()
            self.form_thongke.exec()
        except ImportError:
            self.thong_bao_tam("Thống Kê")