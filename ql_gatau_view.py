import pyodbc
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class QLGaTauView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Danh Mục Ga Tàu")
        self.setMinimumSize(850, 600)
        
        self.init_ui()
        
        # THÊM: Sự kiện nhấn đúp để xem các chuyến tàu đi qua ga này
        self.table_gatau.itemDoubleClicked.connect(self.xem_chuyen_tau_tai_ga)
        
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- 1. KHU VỰC TÌM KIẾM ---
        search_layout = QHBoxLayout()
        self.txt_timkiem = QLineEdit()
        self.txt_timkiem.setPlaceholderText("Nhập tên ga tàu cần tìm...")
        self.btn_tim = QPushButton("🔍 Tìm kiếm")
        self.btn_tim.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px;")
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.txt_timkiem)
        search_layout.addWidget(self.btn_tim)
        main_layout.addLayout(search_layout)

        # Ghi chú nhỏ
        help_label = QLabel("💡 Nhấn đúp vào dòng để xem danh sách các chuyến tàu đi qua ga này.")
        help_label.setStyleSheet("color: gray; font-style: italic;")
        main_layout.addWidget(help_label)

        # --- 2. BẢNG DỮ LIỆU ---
        self.table_gatau = QTableWidget()
        self.table_gatau.setColumnCount(4) # Tăng lên 4 cột để hiện số chuyến tàu
        self.table_gatau.setHorizontalHeaderLabels(["Mã Ga", "Tên Ga", "Địa Chỉ", "Số Chuyến Đang Chạy"])
        self.table_gatau.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_gatau.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_gatau.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.table_gatau)

        # --- 3. KHU VỰC NHẬP LIỆU ---
        bottom_layout = QHBoxLayout()
        form_layout = QFormLayout()
        
        self.txt_maga = QLineEdit()
        self.txt_maga.setPlaceholderText("VD: HNI, SGO...")
        # Tự động viết hoa khi nhập mã ga
        self.txt_maga.textChanged.connect(lambda: self.txt_maga.setText(self.txt_maga.text().upper()))
        
        self.txt_tenga = QLineEdit()
        self.txt_diachi = QLineEdit()

        form_layout.addRow("Mã Ga (*):", self.txt_maga)
        form_layout.addRow("Tên Ga (*):", self.txt_tenga)
        form_layout.addRow("Địa Chỉ:", self.txt_diachi)
        bottom_layout.addLayout(form_layout, stretch=2)

        btn_layout = QVBoxLayout()
        self.btn_them = self.create_button("Thêm Ga Mới", "#2ecc71")
        self.btn_sua = self.create_button("Cập Nhật", "#f39c12")
        self.btn_xoa = self.create_button("Xóa Ga Tàu", "#e74c3c")
        self.btn_clear = self.create_button("Làm Mới Form", "#95a5a6")
        
        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)
        btn_layout.addWidget(self.btn_clear)
        bottom_layout.addLayout(btn_layout, stretch=1)
        
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        # KẾT NỐI SỰ KIỆN
        self.btn_tim.clicked.connect(self.tim_kiem)
        self.btn_them.clicked.connect(self.them_dulieu)
        self.btn_sua.clicked.connect(self.sua_dulieu)
        self.btn_xoa.clicked.connect(self.xoa_dulieu)
        self.btn_clear.clicked.connect(self.clear_form)
        self.table_gatau.cellClicked.connect(self.chon_dulieu)

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"background-color: {color}; color: white; padding: 8px; font-weight: bold; border-radius: 4px;")
        return btn

    # ================= CÁC HÀM XỬ LÝ DATABASE =================

    def load_data(self, query_filter="", params=None):
        self.table_gatau.setRowCount(0)
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # SQL NÂNG CAO: Lấy thông tin Ga kèm theo đếm số chuyến tàu đi qua ga đó
            sql = """
                SELECT G.MaGa, G.TenGa, G.DiaChi, 
                       (SELECT COUNT(*) FROM ChuyenTau C WHERE C.GaDi = G.TenGa OR C.GaDen = G.TenGa) as SoChuyen
                FROM GaTau G
            """
            if query_filter:
                sql += query_filter
                
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            rows = cursor.fetchall()
            for row_idx, row_data in enumerate(rows):
                self.table_gatau.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    val = str(data) if data is not None else ""
                    item = QTableWidgetItem(val)
                    # Căn giữa số chuyến
                    if col_idx == 3:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        if int(data) > 0: item.setForeground(QColor("#2980b9")) # Đổi màu nếu có chuyến
                    self.table_gatau.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))

    def xem_chuyen_tau_tai_ga(self, item):
        """Tính năng mới: Hiển thị các chuyến tàu cụ thể đi qua ga này"""
        row = item.row()
        tenga = self.table_gatau.item(row, 1).text()
        
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            # Tìm các chuyến tàu có Ga Đi hoặc Ga Đến trùng với tên Ga này
            cursor.execute("SELECT MaChuyen, TenChuyen FROM ChuyenTau WHERE GaDi = ? OR GaDen = ?", (tenga, tenga))
            chuyens = cursor.fetchall()
            conn.close()

            if chuyens:
                list_chuyen = "\n".join([f"- {c[0]}: {c[1]}" for c in chuyens])
                QMessageBox.information(self, f"Chuyến tàu tại {tenga}", f"Các chuyến đang khai thác:\n{list_chuyen}")
            else:
                QMessageBox.information(self, "Thông báo", f"Hiện chưa có chuyến tàu nào đi qua ga {tenga}.")
        except: pass

    def clear_form(self):
        self.txt_maga.clear()
        self.txt_maga.setReadOnly(False)
        self.txt_tenga.clear()
        self.txt_diachi.clear()
        self.txt_timkiem.clear()

    def chon_dulieu(self, row, col):
        self.txt_maga.setText(self.table_gatau.item(row, 0).text())
        self.txt_maga.setReadOnly(True)
        self.txt_tenga.setText(self.table_gatau.item(row, 1).text())
        self.txt_diachi.setText(self.table_gatau.item(row, 2).text())

    def tim_kiem(self):
        tukhoa = self.txt_timkiem.text().strip()
        self.load_data(query_filter=" WHERE TenGa LIKE ?", params=(f"%{tukhoa}%",))

    # (Các hàm thêm, sửa, xóa giữ nguyên logic cũ của bạn nhưng đã được tối ưu hiển thị)
    def them_dulieu(self):
        maga, tenga, diachi = self.txt_maga.text().strip(), self.txt_tenga.text().strip(), self.txt_diachi.text().strip()
        if not maga or not tenga: return
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("INSERT INTO GaTau (MaGa, TenGa, DiaChi) VALUES (?, ?, ?)", (maga, tenga, diachi))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def sua_dulieu(self):
        maga, tenga, diachi = self.txt_maga.text().strip(), self.txt_tenga.text().strip(), self.txt_diachi.text().strip()
        if not maga: return
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            conn.execute("UPDATE GaTau SET TenGa=?, DiaChi=? WHERE MaGa=?", (tenga, diachi, maga))
            conn.commit()
            conn.close()
            self.load_data()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def xoa_dulieu(self):
        maga = self.txt_maga.text().strip()
        if not maga: return
        reply = QMessageBox.question(self, 'Xác nhận', f'Xóa Ga: {maga}?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = pyodbc.connect(CONNECTION_STRING)
                conn.execute("DELETE FROM GaTau WHERE MaGa=?", (maga,))
                conn.commit()
                conn.close()
                self.load_data()
            except: QMessageBox.critical(self, "Lỗi", "Không thể xóa Ga đang có Chuyến Tàu chạy qua!")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = QLGaTauView()
    window.show()
    sys.exit(app.exec())