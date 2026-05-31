import pyodbc
import os
import base64  # Thêm thư viện để mã hóa ảnh
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QGroupBox)
from PyQt6.QtCore import Qt

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class BanVeQuayView(QDialog):
    def __init__(self, staff_id, staff_name):
        super().__init__()
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.setWindowTitle("Phần Mềm Quản Lý Bán Vé - Nghiệp Vụ Tại Quầy")
        self.setFixedSize(550, 550)
        self.init_ui()
        self.load_chuyen_tau()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        lbl_title = QLabel(f"🚂 BÁN VÉ TRỰC TIẾP TẠI QUẦY")
        lbl_title.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 20px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_title)
        
        lbl_staff = QLabel(f"Nhân viên phụ trách: {self.staff_name.upper()}")
        lbl_staff.setStyleSheet("color: #7f8c8d; font-size: 13px; font-style: italic; margin-bottom: 10px;")
        lbl_staff.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_staff)

        # KHU VỰC THÔNG TIN CHUYẾN & GHẾ
        group_ve = QGroupBox("Chi Tiết Chuyến Đi")
        group_ve.setStyleSheet("QGroupBox { font-weight: bold; color: #2980b9; border: 1px solid #bdc3c7; border-radius: 5px; margin-top: 10px; padding-top: 15px; }")
        layout_ve = QFormLayout()
        
        self.cb_chuyentau = QComboBox()
        self.cb_chuyentau.setStyleSheet("padding: 5px;")
        self.cb_chuyentau.currentIndexChanged.connect(self.cap_nhat_ghe_trong)
        
        self.cb_loaighe = QComboBox()
        self.cb_loaighe.addItems(["Ngồi Cứng", "Ngồi Mềm Điều Hòa", "Giường Nằm Khoang 4", "Giường Nằm Khoang 6"])
        self.cb_loaighe.setStyleSheet("padding: 5px;")
        self.cb_loaighe.currentIndexChanged.connect(self.cap_nhat_ghe_trong)
        
        self.cb_soghe = QComboBox()
        self.cb_soghe.setStyleSheet("padding: 5px; font-weight: bold; color: #d35400;")
        
        layout_ve.addRow("Lựa chọn Chuyến Tàu:", self.cb_chuyentau)
        layout_ve.addRow("Loại Khoang / Ghế:", self.cb_loaighe)
        layout_ve.addRow("Vị trí Ghế (Trống):", self.cb_soghe)
        group_ve.setLayout(layout_ve)
        main_layout.addWidget(group_ve)

        # KHU VỰC THÔNG TIN KHÁCH HÀNG
        group_kh = QGroupBox("Hành Khách & Thanh Toán")
        group_kh.setStyleSheet("QGroupBox { font-weight: bold; color: #27ae60; border: 1px solid #bdc3c7; border-radius: 5px; margin-top: 10px; padding-top: 15px; }")
        layout_kh = QFormLayout()
        
        self.txt_tenhk = QLineEdit()
        self.txt_tenhk.setPlaceholderText("Nhập họ tên in trên thẻ CCCD...")
        self.txt_tenhk.setStyleSheet("padding: 5px;")
        
        self.txt_cccd = QLineEdit()
        self.txt_cccd.setPlaceholderText("Nhập số CCCD / Hộ chiếu...")
        self.txt_cccd.setStyleSheet("padding: 5px;")

        self.cb_thanhtoan = QComboBox()
        self.cb_thanhtoan.addItems(["💵 Tiền mặt", "📲 Chuyển khoản (Quét QR)", "💳 Quẹt thẻ ngân hàng (POS)"])
        self.cb_thanhtoan.setStyleSheet("padding: 5px; font-weight: bold; color: #16a085;")

        layout_kh.addRow("Họ và Tên (*):", self.txt_tenhk)
        layout_kh.addRow("Số Giấy Tờ (*):", self.txt_cccd)
        layout_kh.addRow("Thanh Toán Bằng:", self.cb_thanhtoan)
        group_kh.setLayout(layout_kh)
        main_layout.addWidget(group_kh)

        main_layout.addSpacing(15)

        self.btn_banve = QPushButton("💵 THANH TOÁN & IN VÉ ĐIỆN TỬ")
        self.btn_banve.setFixedSize(300, 50)
        self.btn_banve.setStyleSheet("""
            QPushButton { background-color: #e74c3c; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_banve, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.btn_banve.clicked.connect(self.thuc_hien_ban_ve)

    def load_chuyen_tau(self):
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT MaChuyen, TenChuyen FROM ChuyenTau")
            for row in cursor.fetchall():
                self.cb_chuyentau.addItem(f"{row[0]} - {row[1]}", row[0])
            conn.close()
            self.cap_nhat_ghe_trong() 
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Chuyến Tàu", str(e))

    def cap_nhat_ghe_trong(self):
        self.cb_soghe.clear()
        ma_chuyen = self.cb_chuyentau.currentData()
        loai_khoang = self.cb_loaighe.currentText()
        if not ma_chuyen: return

        ghe_da_ban = []
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT LoaiGhe FROM VeTau WHERE MaChuyen=?", (ma_chuyen,))
            for row in cursor.fetchall():
                thong_tin_ghe_db = row[0] 
                if loai_khoang in thong_tin_ghe_db:
                    parts = thong_tin_ghe_db.split("Ghế ")
                    if len(parts) == 2:
                        ghe_da_ban.append(parts[1].strip())
            conn.close()
        except Exception: pass

        for i in range(1, 61):
            so_ghe = f"{i:02d}"
            if so_ghe not in ghe_da_ban:
                self.cb_soghe.addItem(f"{so_ghe}")

        if self.cb_soghe.count() == 0:
            self.cb_soghe.addItem("HẾT CHỖ")
            self.cb_soghe.setEnabled(False)
            self.btn_banve.setEnabled(False)
        else:
            self.cb_soghe.setEnabled(True)
            self.btn_banve.setEnabled(True)

    def thuc_hien_ban_ve(self):
        ma_chuyen = self.cb_chuyentau.currentData()
        ten_chuyen = self.cb_chuyentau.currentText()
        
        so_ghe = self.cb_soghe.currentText()
        if so_ghe == "HẾT CHỖ": return
        
        loai_ghe = self.cb_loaighe.currentText()
        thong_tin_ghe = f"{loai_ghe} - Ghế {so_ghe}"
        
        ten = self.txt_tenhk.text().strip()
        cccd = self.txt_cccd.text().strip()
        hinh_thuc_tt = self.cb_thanhtoan.currentText()

        if not ten or not cccd:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin khách hàng!")
            return

        ngay_dat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO VeTau (MaChuyen, TenHanhKhach, CCCD, LoaiGhe, NgayDat, BookingChannel, StaffID) 
                VALUES (?, ?, ?, ?, ?, 'Offline', ?)
            """, (ma_chuyen, ten, cccd, thong_tin_ghe, ngay_dat, self.staff_id))
            
            cursor.execute("SELECT @@IDENTITY")
            ma_ve = int(cursor.fetchone()[0])
            conn.commit()
            conn.close()

            self.in_ve_html(ma_ve, ten, cccd, ten_chuyen, loai_ghe, so_ghe, ngay_dat, hinh_thuc_tt)
            
            QMessageBox.information(self, "Thành công", f"Giao dịch thành công! Vé đã được in.")
            self.txt_tenhk.clear()
            self.txt_cccd.clear()
            self.cap_nhat_ghe_trong() 
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", str(e))

    # ================= XUẤT VÉ ĐIỆN TỬ (CÓ TÍCH HỢP MÃ QR DẠNG BASE64) =================
    def in_ve_html(self, ma_ve, ten, cccd, ten_chuyen, loai_khoang, so_ghe, ngay_dat, hinh_thuc_tt):
        if not os.path.exists("HoaDon"):
            os.makedirs("HoaDon")
            
        ten_file = os.path.abspath(f"HoaDon/VeDienTu_{ma_ve}.html")
        
        # ĐIỂM THAY ĐỔI: Mã hóa ảnh ra Base64 để nhúng thẳng vào HTML
        qr_html = ""
        if "Chuyển khoản" in hinh_thuc_tt:
            qr_path = os.path.abspath("qr_code.jpg")
            if os.path.exists(qr_path):
                with open(qr_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
                qr_html = f"""
                <div style="margin-top: 10px; text-align: right;">
                    <p style="font-size: 11px; color: #e74c3c; margin: 0 0 5px 0; font-weight: bold;">Quét QR thanh toán</p>
                    <img src="data:image/jpeg;base64,{encoded_string}" alt="QR Code" style="width: 120px; border-radius: 8px; border: 2px solid #bdc3c7; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                </div>
                """
            else:
                qr_html = """
                <div style="margin-top: 10px; text-align: right;">
                    <p style="font-size: 11px; color: #e74c3c; margin: 0 0 5px 0; font-weight: bold;">(Thiếu file qr_code.jpg)</p>
                </div>
                """
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <title>Vé Điện Tử - {ma_ve}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #ecf0f1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .ticket-box {{ background: white; width: 650px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #bdc3c7; }}
                .header {{ background-color: #2980b9; color: white; padding: 20px; text-align: center; border-bottom: 4px solid #f39c12; }}
                .header h1 {{ margin: 0; font-size: 26px; letter-spacing: 2px; text-transform: uppercase; }}
                .header p {{ margin: 5px 0 0; opacity: 0.9; font-size: 14px; }}
                .content {{ padding: 30px; display: flex; justify-content: space-between; }}
                .info-left {{ width: 55%; }}
                .info-right {{ width: 40%; text-align: right; border-left: 2px dashed #bdc3c7; padding-left: 20px; }}
                h3 {{ color: #7f8c8d; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px; }}
                p.val {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 0; margin-bottom: 20px; }}
                .seat-box {{ background: #f39c12; color: white; padding: 10px 15px; border-radius: 8px; display: inline-block; font-size: 26px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .payment-box {{ background: #e8f8f5; border: 1px solid #1abc9c; color: #16a085; padding: 6px 12px; border-radius: 4px; display: inline-block; font-size: 14px; font-weight: bold; margin-bottom: 10px; }}
                .footer {{ background: #ecf0f1; padding: 15px; text-align: center; font-size: 13px; color: #34495e; border-top: 1px solid #bdc3c7; }}
                .barcode {{ font-family: 'Libre Barcode 39', cursive, monospace; font-size: 40px; color: #2c3e50; margin-top: 15px; letter-spacing: 4px; }}
            </style>
        </head>
        <body>
            <div class="ticket-box">
                <div class="header">
                    <h1>🚂 THẺ LÊN TÀU HỎA</h1>
                    <p>Mã đặt chỗ / PNR: <strong>#{ma_ve:06d}</strong> &nbsp;|&nbsp; Phục vụ bởi: <strong>{self.staff_name}</strong></p>
                </div>
                <div class="content">
                    <div class="info-left">
                        <h3>Hành khách / Passenger</h3>
                        <p class="val">{ten.upper()}</p>
                        
                        <h3>Giấy tờ / ID Card</h3>
                        <p class="val">{cccd}</p>
                        
                        <h3>Chuyến tàu / Train</h3>
                        <p class="val">{ten_chuyen}</p>
                        
                        <h3>Khoang / Class</h3>
                        <p class="val" style="margin-bottom: 0;">{loai_khoang}</p>
                    </div>
                    <div class="info-right">
                        <h3>Ngày xuất vé / Date</h3>
                        <p style="font-size: 15px; color: #2c3e50; font-weight: bold; margin-top: 0; margin-bottom: 15px;">{ngay_dat}</p>
                        
                        <h3>Thanh toán / Payment</h3>
                        <div class="payment-box">{hinh_thuc_tt}</div>
                        
                        {qr_html}
                        
                        <h3 style="margin-top: 15px;">Số Ghế / Seat</h3>
                        <div class="seat-box">{so_ghe}</div>
                        
                        <div class="barcode">*{ma_ve:06d}*</div>
                    </div>
                </div>
                <div class="footer">
                    <strong>Lưu ý:</strong> Vui lòng xuất trình thẻ này cùng giấy tờ tùy thân khi lên tàu. Chúc Quý khách thượng lộ bình an!
                </div>
            </div>
            <script> window.onload = function() {{ window.print(); }} </script>
        </body>
        </html>
        """
        with open(ten_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        os.startfile(ten_file)