import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLKhachHangView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Thông Tin Khách Hàng")
        self.setMinimumSize(750, 500)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- 1. KHU VỰC TÌM KIẾM ---
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập tên hoặc SĐT khách hàng...")
        self.btn_tim = QPushButton("Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # --- 2. BẢNG DỮ LIỆU ---
        self.table_kh = QTableWidget()
        self.table_kh.setColumnCount(4)
        self.table_kh.setHorizontalHeaderLabels(["Mã KH", "Tên Khách Hàng", "CCCD", "Số Điện Thoại"])
        self.table_kh.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table_kh)

        # --- 3. KHU VỰC NHẬP LIỆU & NÚT BẤM ---
        bottom_layout = QHBoxLayout()
        
        form_layout = QFormLayout()
        self.txt_makh = QLineEdit()
        self.txt_tenkh = QLineEdit()
        self.txt_cccd = QLineEdit()
        self.txt_sdt = QLineEdit()

        form_layout.addRow("Mã KH (*):", self.txt_makh)
        form_layout.addRow("Tên KH (*):", self.txt_tenkh)
        form_layout.addRow("CCCD/CMND:", self.txt_cccd)
        form_layout.addRow("Số ĐT:", self.txt_sdt)
        bottom_layout.addLayout(form_layout, stretch=2)

        btn_layout = QVBoxLayout()
        self.btn_them = QPushButton("Thêm Khách Hàng")
        self.btn_sua = QPushButton("Cập Nhật")
        self.btn_xoa = QPushButton("Xóa Khách Hàng")
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
        self.table_kh.cellClicked.connect(self.chon_dulieu)

    # ================= CÁC HÀM XỬ LÝ DATABASE =================

    def load_data(self, query_filter="", params=None):
        self.table_kh.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = "SELECT MaKH, TenKH, CCCD, SDT FROM KhachHang"
            if query_filter:
                sql += query_filter
                
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_kh.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    self.table_kh.setItem(row_idx, col_idx, QTableWidgetItem(val))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))
        self.clear_form()

    def clear_form(self):
        self.txt_makh.clear()
        self.txt_makh.setReadOnly(False)
        self.txt_tenkh.clear()
        self.txt_cccd.clear()
        self.txt_sdt.clear()
        self.txt_timkiem.clear()

    def chon_dulieu(self, row, col):
        self.txt_makh.setText(self.table_kh.item(row, 0).text())
        self.txt_makh.setReadOnly(True)
        self.txt_tenkh.setText(self.table_kh.item(row, 1).text())
        self.txt_cccd.setText(self.table_kh.item(row, 2).text())
        self.txt_sdt.setText(self.table_kh.item(row, 3).text())

    def them_dulieu(self):
        ma = self.txt_makh.text().strip()
        ten = self.txt_tenkh.text().strip()
        cccd = self.txt_cccd.text().strip()
        sdt = self.txt_sdt.text().strip()

        if not ma or not ten:
            QMessageBox.warning(self, "Lỗi", "Mã KH và Tên KH không được để trống!")
            return

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO KhachHang (MaKH, TenKH, CCCD, SDT) VALUES (?, ?, ?, ?)", (ma, ten, cccd, sdt))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm khách hàng!")
            self.load_data()
        except pyodbc.IntegrityError:
            QMessageBox.warning(self, "Lỗi", "Mã KH này đã tồn tại!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def sua_dulieu(self):
        ma = self.txt_makh.text().strip()
        if not ma: return
        ten = self.txt_tenkh.text().strip()
        cccd = self.txt_cccd.text().strip()
        sdt = self.txt_sdt.text().strip()

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("UPDATE KhachHang SET TenKH=?, CCCD=?, SDT=? WHERE MaKH=?", (ten, cccd, sdt, ma))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_dulieu(self):
        ma = self.txt_makh.text().strip()
        if not ma: return
        reply = QMessageBox.question(self, 'Xác nhận', f'Xóa Khách Hàng: {ma}?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                conn.execute("DELETE FROM KhachHang WHERE MaKH=?", (ma,))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa (có thể khách hàng này đã có hóa đơn/vé).")

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(query_filter=" WHERE TenKH LIKE ? OR SDT LIKE ?", params=(f"%{tukhoa}%", f"%{tukhoa}%"))