import sys
from PyQt6.QtWidgets import QApplication
from views.dangnhap_view import DangNhapView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Khởi động Form Đăng Nhập đầu tiên
    main_window = DangNhapView()
    main_window.show()
    
    sys.exit(app.exec())