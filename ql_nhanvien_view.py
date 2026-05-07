import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLNhanVienView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Thông Tin Nhân Sự")
        self.setMinimumSize(750, 500)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- 1. KHU VỰC TÌM KIẾM ---
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập mã hoặc tên nhân viên...")
        self.btn_tim = QPushButton("Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # --- 2. BẢNG DỮ LIỆU ---
        self.table_nv = QTableWidget()
        self.table_nv.setColumnCount(4)
        self.table_nv.setHorizontalHeaderLabels(["Mã NV", "Tên Nhân Viên", "Chức Vụ", "Số Điện Thoại"])
        self.table_nv.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_nv)

        # --- 3. KHU VỰC NHẬP LIỆU & NÚT BẤM ---
        bottom_layout = QHBoxLayout()
        
        form_layout = QFormLayout()
        self.txt_manv = QLineEdit()
        self.txt_tennv = QLineEdit()
        self.txt_chucvu = QLineEdit()
        self.txt_sdt = QLineEdit()

        form_layout.addRow("Mã NV (*):", self.txt_manv)
        form_layout.addRow("Tên NV (*):", self.txt_tennv)
        form_layout.addRow("Chức vụ:", self.txt_chucvu)
        form_layout.addRow("Số ĐT:", self.txt_sdt)
        bottom_layout.addLayout(form_layout, stretch=2)

        btn_layout = QVBoxLayout()
        self.btn_them = QPushButton("Thêm Nhân Viên")
        self.btn_sua = QPushButton("Cập Nhật")
        self.btn_xoa = QPushButton("Xóa Nhân Viên")
        self.btn_clear = QPushButton("Làm Mới Form")
        
        self.btn_them.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        self.btn_sua.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        self.btn_xoa.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        
        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)
        btn_layout.addWidget(self.btn_clear)
        bottom_layout.addLayout(btn_layout, stretch=1)
        
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        # --- KẾT NỐI SỰ KIỆN ---
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_clear.clicked.connect(self.clear_form)
        self.table_nv.cellClicked.connect(self.chon_dulieu)

    # ================= CÁC HÀM XỬ LÝ DATABASE =================

    def load_data(self, query_filter="", params=None):
        self.table_nv.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = "SELECT MaNV, TenNV, ChucVu, SDT FROM NhanVien"
            if query_filter:
                sql += query_filter
                
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_nv.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_nv.setItem(row_idx, col_idx, QTableWidgetItem(val))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))
        self.clear_form()

    def clear_form(self):
        self.txt_manv.clear()
        self.txt_manv.setReadOnly(False)
        self.txt_tennv.clear()
        self.txt_chucvu.clear()
        self.txt_sdt.clear()
        self.txt_timkiem.clear()

    def chon_dulieu(self, row, col):
        self.txt_manv.setText(self.table_nv.item(row, 0).text())
        self.txt_manv.setReadOnly(True)
        self.txt_tennv.setText(self.table_nv.item(row, 1).text())
        self.txt_chucvu.setText(self.table_nv.item(row, 2).text())
        self.txt_sdt.setText(self.table_nv.item(row, 3).text())

    def them_dulieu(self):
        ma = self.txt_manv.text().strip()
        ten = self.txt_tennv.text().strip()
        chucvu = self.txt_chucvu.text().strip()
        sdt = self.txt_sdt.text().strip()

        if not ma or not ten:
            QMessageBox.warning(self, "Lỗi", "Mã NV và Tên NV không được để trống!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO NhanVien (MaNV, TenNV, ChucVu, SDT) VALUES (?, ?, ?, ?)", (ma, ten, chucvu, sdt))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm nhân viên!")
            self.load_data()
        except pyodbc.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã NV này đã tồn tại!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def sua_dulieu(self):
        ma = self.txt_manv.text().strip()
        if not ma: return
        ten = self.txt_tennv.text().strip()
        chucvu = self.txt_chucvu.text().strip()
        sdt = self.txt_sdt.text().strip()

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("UPDATE NhanVien SET TenNV=?, ChucVu=?, SDT=? WHERE MaNV=?", (ten, chucvu, sdt, ma))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_dulieu(self):
        ma = self.txt_manv.text().strip()
        if not ma: return
        reply = QMessageBox.question(self, 'Xác nhận', f'Xóa Nhân Viên: {ma}?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                conn.execute("DELETE FROM NhanVien WHERE MaNV=?", (ma,))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa nhân viên này.")

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(query_filter=" WHERE TenNV LIKE ? OR MaNV LIKE ?", params=(f"%{tukhoa}%", f"%{tukhoa}%"))