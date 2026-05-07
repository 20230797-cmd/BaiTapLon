import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QComboBox, QHeaderView)
from PyQt6.QtCore import Qt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLTaiKhoanView(QDialog):
    def __init__(self, current_admin_id):
        super().__init__()
        self.admin_id = current_admin_id # Lưu ID của người đang đăng nhập (để làm cột CreatedBy)
        
        self.setWindowTitle("Quản Lý Người Dùng Hệ Thống")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 1. KHU VỰC TÌM KIẾM (Trên cùng)
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập tên tài khoản cần tìm...")
        self.btn_tim = QPushButton("Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # 2. KHU VỰC BẢNG DỮ LIỆU (Ở giữa)
        self.table_taikhoan = QTableWidget()
        self.table_taikhoan.setColumnCount(5)
        self.table_taikhoan.setHorizontalHeaderLabels(["Username", "Họ Tên", "SĐT", "Quyền", "Người Tạo"])
        # Cho bảng tự động giãn cột lấp đầy khoảng trống
        self.table_taikhoan.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_taikhoan)

        # 3. KHU VỰC NHẬP LIỆU & NÚT BẤM (Dưới cùng)
        bottom_layout = QHBoxLayout()
        
        # 3.1 Form nhập liệu (Bên trái)
        form_layout = QFormLayout()
        self.txt_username = QLineEdit()
        self.txt_password = QLineEdit()
        self.txt_hoten = QLineEdit()
        self.txt_phone = QLineEdit()
        self.cb_role = QComboBox()
        self.cb_role.addItems(["User", "Staff", "Admin"])

        form_layout.addRow("Tài khoản (*):", self.txt_username)
        form_layout.addRow("Mật khẩu (*):", self.txt_password)
        form_layout.addRow("Họ tên (*):", self.txt_hoten)
        form_layout.addRow("Số điện thoại:", self.txt_phone)
        form_layout.addRow("Phân quyền:", self.cb_role)
        
        bottom_layout.addLayout(form_layout, stretch=2) # Chiếm 2 phần không gian

        # 3.2 Các nút thao tác (Bên phải)
        btn_layout = QVBoxLayout()
        self.btn_them = self.create_button("Thêm Tài Khoản", "#2ecc71")
        self.btn_sua = self.create_button("Cập Nhật", "#f39c12")
        self.btn_xoa = self.create_button("Xóa Tài Khoản", "#e74c3c")
        self.btn_clear = self.create_button("Làm Mới Form", "#95a5a6")
        
        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)
        btn_layout.addWidget(self.btn_clear)
        
        bottom_layout.addLayout(btn_layout, stretch=1) # Chiếm 1 phần không gian
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # KẾT NỐI SỰ KIỆN
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.btn_them.clicked.connect(self.them_tai_khoan)
        self.btn_sua.clicked.connect(self.sua_tai_khoan)
        self.btn_xoa.clicked.connect(self.xoa_tai_khoan)
        self.btn_clear.clicked.connect(self.clear_form)
        self.table_taikhoan.cellClicked.connect(self.chon_dulieu)

    def create_button(self, text, color):
        """Hàm tạo nút nhanh"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"background-color: {color}; color: white; padding: 8px; font-weight: bold; border-radius: 4px;")
        return btn

    # ================= CÁC HÀM XỬ LÝ DATABASE =================

    def load_data(self, query_filter="", params=None):
        self.table_taikhoan.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # LEFT JOIN để lấy tên người tạo (Creator) thay vì chỉ lấy ID
            sql = """
                SELECT u1.Username, u1.FullName, u1.Phone, u1.Role, u2.Username as Creator
                FROM Users u1
                LEFT JOIN Users u2 ON u1.CreatedBy = u2.UserID
            """
            if query_filter:
                sql += " WHERE u1.Username LIKE ?"
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_taikhoan.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(val))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))
            
        self.clear_form()

    def clear_form(self):
        self.txt_username.clear()
        self.txt_username.setReadOnly(False) # Mở khóa ô nhập Username
        self.txt_password.clear()
        self.txt_hoten.clear()
        self.txt_phone.clear()
        self.cb_role.setCurrentIndex(0)
        self.txt_timkiem.clear()

    def chon_dulieu(self, row, col):
        """Khi click vào bảng, đẩy dữ liệu xuống form bên dưới"""
        self.txt_username.setText(self.table_taikhoan.item(row, 0).text())
        self.txt_username.setReadOnly(True) # Không cho sửa tên đăng nhập
        self.txt_password.setPlaceholderText("(Bỏ trống nếu không đổi mật khẩu)")
        self.txt_hoten.setText(self.table_taikhoan.item(row, 1).text())
        self.txt_phone.setText(self.table_taikhoan.item(row, 2).text())
        
        role_text = self.table_taikhoan.item(row, 3).text()
        index = self.cb_role.findText(role_text)
        if index >= 0:
            self.cb_role.setCurrentIndex(index)

    def them_tai_khoan(self):
        user = self.txt_username.text().strip()
        pwd = self.txt_password.text().strip()
        hoten = self.txt_hoten.text().strip()
        sdt = self.txt_phone.text().strip()
        role = self.cb_role.currentText()

        if not user or not pwd or not hoten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ các trường có dấu (*)!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # Kiểm tra trùng lặp
            cursor.execute("SELECT Username FROM Users WHERE Username=?", (user,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "Tài khoản này đã tồn tại!")
                conn.close()
                return

            query = "INSERT INTO Users (Username, Password, FullName, Phone, Role, CreatedBy) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (user, pwd, hoten, sdt, role, self.admin_id))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Thành công", f"Đã cấp tài khoản {role} thành công!")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def sua_tai_khoan(self):
        user = self.txt_username.text().strip()
        pwd = self.txt_password.text().strip()
        hoten = self.txt_hoten.text().strip()
        sdt = self.txt_phone.text().strip()
        role = self.cb_role.currentText()

        if not user or not hoten:
            QMessageBox.warning(self, "Lỗi", "Tài khoản và Họ tên không được để trống!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            # Nếu có nhập mật khẩu mới thì cập nhật cả mật khẩu, ngược lại giữ nguyên MK cũ
            if pwd:
                query = "UPDATE Users SET Password=?, FullName=?, Phone=?, Role=? WHERE Username=?"
                conn.execute(query, (pwd, hoten, sdt, role, user))
            else:
                query = "UPDATE Users SET FullName=?, Phone=?, Role=? WHERE Username=?"
                conn.execute(query, (hoten, sdt, role, user))
                
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin tài khoản!")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_tai_khoan(self):
        user = self.txt_username.text().strip()
        if not user: return
        
        if user.lower() == 'admin':
            QMessageBox.warning(self, "Cảnh báo", "Tuyệt đối không được xóa tài khoản Admin gốc!")
            return
            
        reply = QMessageBox.question(self, 'Xác nhận', f'Chắc chắn muốn xóa tài khoản {user}?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                conn.execute("DELETE FROM Users WHERE Username=?", (user,))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa do ràng buộc dữ liệu (Tài khoản này đã lập hóa đơn/vé).")

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(query_filter="WHERE u1.Username LIKE ?", params=(f"%{tukhoa}%",))