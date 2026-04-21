from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox

class MenuKhachHangView(QtWidgets.QDialog):
    def __init__(self, username_dang_nhap):
        super().__init__()
        # Tải giao diện Menu Khách Hàng (3 nút)
        uic.loadUi('ui/MenuKhachHang.ui', self)
        
        self.username = username_dang_nhap
        self.setWindowTitle(f"Xin chào Khách hàng: {self.username}")
        
        # Kết nối các nút bấm
        self.btn_datve.clicked.connect(self.mo_form_dat_ve)
        self.btn_lichsu.clicked.connect(lambda: QMessageBox.information(self, "Thông báo", "Sẽ mở Lịch sử vé ở bản cập nhật sau!"))
        self.btn_doimatkhau.clicked.connect(lambda: QMessageBox.information(self, "Thông báo", "Sẽ mở Đổi mật khẩu ở bản cập nhật sau!"))

    def mo_form_dat_ve(self):
        # Mở form Đặt Vé (Cần đảm bảo bạn đã tạo file datve_khachhang_view.py)
        try:
            from views.datve_khachhang_view import DatVeKhachHangView
            self.form_datve = DatVeKhachHangView(self.username)
            self.form_datve.exec()
        except ImportError:
            QMessageBox.warning(self, "Lỗi", "Chưa tìm thấy file views/datve_khachhang_view.py. Bạn hãy tạo nó nhé!")