import pyodbc
import os
import base64
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QGroupBox)
from PyQt6.QtCore import Qt

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONNECTION_STRING

class DatVeKhachHangView(QDialog):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.setWindowTitle(f"Đặt Vé Trực Tuyến - {username.upper()}")
        self.setFixedSize(600, 550)
        self.init_ui()
        self.load_chuyen_tau()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. TIÊU ĐỀ
        lbl_title = QLabel(f"🚂 CỔNG ĐẶT VÉ TRỰC TUYẾN DÀNH CHO HÀNH KHÁCH")
        lbl_title.setStyleSheet("font-weight: bold; color: #e67e22; font-size: 18px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_title)

        # 2. KHU VỰC THÔNG TIN CHUYẾN & GHẾ
        group_ve = QGroupBox("1. Lựa Chọn Chuyến Đi & Vị Trí")
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
        
        layout_ve.addRow("Chọn Chuyến Tàu:", self.cb_chuyentau)
        layout_ve.addRow("Chọn Loại Khoang:", self.cb_loaighe)
        layout_ve.addRow("Chọn Ghế (Đang Trống):", self.cb_soghe)
        group_ve.setLayout(layout_ve)
        main_layout.addWidget(group_ve)

        # 3. KHU VỰC THÔNG TIN KHÁCH HÀNG & THANH TOÁN
        group_kh = QGroupBox("2. Thông Tin Hành Khách & Thanh Toán")
        group_kh.setStyleSheet("QGroupBox { font-weight: bold; color: #27ae60; border: 1px solid #bdc3c7; border-radius: 5px; margin-top: 10px; padding-top: 15px; }")
        layout_kh = QFormLayout()
        
        self.txt_tenhk = QLineEdit()
        self.txt_tenhk.setPlaceholderText("Họ và tên in trên CCCD (Bắt buộc)...")
        self.txt_tenhk.setStyleSheet("padding: 5px;")
        
        self.txt_cccd = QLineEdit()
        self.txt_cccd.setPlaceholderText("Số Giấy Tờ Tùy Thân (Bắt buộc)...")
        self.txt_cccd.setStyleSheet("padding: 5px;")

        self.cb_thanhtoan = QComboBox()
        self.cb_thanhtoan.addItems(["MoMo E-Wallet", "VNPay", "ZaloPay", "Thẻ Tín Dụng / Ghi Nợ (Visa/Master)"])
        self.cb_thanhtoan.setStyleSheet("padding: 5px; font-weight: bold; color: #8e44ad;")

        layout_kh.addRow("Họ và Tên:", self.txt_tenhk)
        layout_kh.addRow("Số Giấy Tờ (CCCD):", self.txt_cccd)
        layout_kh.addRow("Phương Thức Thanh Toán:", self.cb_thanhtoan)
        group_kh.setLayout(layout_kh)
        main_layout.addWidget(group_kh)

        main_layout.addSpacing(15)

        # 4. NÚT CHỐT VÉ
        self.btn_banve = QPushButton("🔒 XÁC NHẬN THANH TOÁN & XUẤT VÉ")
        self.btn_banve.setFixedSize(350, 50)
        self.btn_banve.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_banve, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.btn_banve.clicked.connect(self.thuc_hien_ban_ve)

    # ================= CÁC HÀM XỬ LÝ DATABASE =================

    def load_chuyen_tau(self):
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute("SELECT MaChuyen, TenChuyen, NgayDi FROM ChuyenTau")
            for row in cursor.fetchall():
                # Hiện thêm ngày đi cho khách hàng dễ nhìn
                ngay_di = row[2] if row[2] else "Chưa rõ ngày"
                self.cb_chuyentau.addItem(f"{row[0]} - {row[1]} (Khởi hành: {ngay_di})", row[0])
            conn.close()
            self.cap_nhat_ghe_trong() 
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tải Chuyến Tàu", str(e))

    def cap_nhat_ghe_trong(self):
        """Thuật toán quét DB để loại bỏ những ghế đã được mua (Y hệt bên Nhân viên)"""
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
        # Cắt bớt phần '(Khởi hành...)' để lấy tên tàu thuần túy in ra vé
        ten_chuyen_full = self.cb_chuyentau.currentText()
        ten_chuyen = ten_chuyen_full.split(" (Khởi hành:")[0]
        
        so_ghe = self.cb_soghe.currentText()
        if so_ghe == "HẾT CHỖ": return
        
        loai_ghe = self.cb_loaighe.currentText()
        thong_tin_ghe = f"{loai_ghe} - Ghế {so_ghe}"
        
        ten = self.txt_tenhk.text().strip()
        cccd = self.txt_cccd.text().strip()
        hinh_thuc_tt = self.cb_thanhtoan.currentText()

        if not ten or not cccd:
            QMessageBox.warning(self, "Lỗi", "Quý khách vui lòng nhập đầy đủ Họ tên và số CCCD!")
            return

        ngay_dat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            # ĐIỂM QUAN TRỌNG: BookingChannel = 'Online', StaffID = NULL (Khách tự mua)
            cursor.execute("""
                INSERT INTO VeTau (MaChuyen, TenHanhKhach, CCCD, LoaiGhe, NgayDat, BookingChannel, StaffID) 
                VALUES (?, ?, ?, ?, ?, 'Online', NULL)
            """, (ma_chuyen, ten, cccd, thong_tin_ghe, ngay_dat))
            
            cursor.execute("SELECT @@IDENTITY")
            ma_ve = int(cursor.fetchone()[0])
            conn.commit()
            conn.close()

            # Mở trình duyệt in Vé điện tử Online
            self.in_ve_html_online(ma_ve, ten, cccd, ten_chuyen, loai_ghe, so_ghe, ngay_dat, hinh_thuc_tt)
            
            QMessageBox.information(self, "Thanh Toán Thành Công", f"Giao dịch Online thành công!\nHệ thống đang mở Vé Điện Tử. Quý khách vui lòng chụp màn hình hoặc lưu file PDF để sử dụng khi lên tàu.")
            self.txt_tenhk.clear()
            self.txt_cccd.clear()
            self.cap_nhat_ghe_trong() # Trừ ghế trống ngay lập tức
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", str(e))

    # ================= XUẤT VÉ ĐIỆN TỬ DÀNH CHO KHÁCH HÀNG =================
    def in_ve_html_online(self, ma_ve, ten, cccd, ten_chuyen, loai_khoang, so_ghe, ngay_dat, hinh_thuc_tt):
        if not os.path.exists("HoaDon"):
            os.makedirs("HoaDon")
            
        ten_file = os.path.abspath(f"HoaDon/E-Ticket_Online_{ma_ve}.html")
        
        # ĐIỂM THAY ĐỔI: Dùng thẻ <img> mã hóa Base64 ảnh QR để khách hàng lưu vé không bị mất ảnh.
        qr_html = ""
        qr_path = os.path.abspath("qr_code.jpg")
        if os.path.exists(qr_path):
            with open(qr_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            qr_html = f"""
            <div style="margin-top: 15px; text-align: center;">
                <p style="font-size: 11px; color: #7f8c8d; margin: 0 0 5px 0;">Mã QR soát vé tự động</p>
                <img src="data:image/jpeg;base64,{encoded_string}" alt="QR Soát Vé" style="width: 100px; height: 100px; border-radius: 5px; border: 1px solid #bdc3c7;">
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <title>E-Ticket: {ma_ve}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #34495e; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .ticket-box {{ background: white; width: 650px; border-radius: 12px; box-shadow: 0 15px 25px rgba(0,0,0,0.3); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 25px; text-align: center; position: relative; }}
                .header h1 {{ margin: 0; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; }}
                .badge-online {{ background-color: #f1c40f; color: #c0392b; font-size: 12px; font-weight: bold; padding: 5px 10px; border-radius: 15px; position: absolute; top: 20px; right: 20px; }}
                .content {{ padding: 30px; display: flex; justify-content: space-between; }}
                .info-left {{ width: 55%; }}
                .info-right {{ width: 40%; text-align: right; border-left: 2px dashed #bdc3c7; padding-left: 20px; }}
                h3 {{ color: #95a5a6; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px; }}
                p.val {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 0; margin-bottom: 20px; }}
                .seat-box {{ background: #e74c3c; color: white; padding: 10px 15px; border-radius: 8px; display: inline-block; font-size: 26px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .payment-box {{ background: #f8f9fa; border: 1px solid #ced4da; color: #495057; padding: 6px 12px; border-radius: 4px; display: inline-block; font-size: 13px; font-weight: bold; margin-bottom: 10px; }}
                .footer {{ background: #ecf0f1; padding: 15px; text-align: center; font-size: 13px; color: #34495e; border-top: 1px dashed #bdc3c7; }}
                .barcode {{ font-family: 'Libre Barcode 39', cursive, monospace; font-size: 40px; color: #2c3e50; margin-top: 10px; letter-spacing: 4px; }}
            </style>
        </head>
        <body>
            <div class="ticket-box">
                <div class="header">
                    <h1>🚂 VÉ TÀU ĐIỆN TỬ (E-TICKET)</h1>
                    <p style="margin: 5px 0 0; opacity: 0.9; font-size: 14px;">Mã Đặt Chỗ: <strong>#{ma_ve:06d}</strong></p>
                    <span class="badge-online">MUA ONLINE</span>
                </div>
                <div class="content">
                    <div class="info-left">
                        <h3>Hành khách / Passenger</h3>
                        <p class="val">{ten.upper()}</p>
                        
                        <h3>Số Giấy Tờ / ID</h3>
                        <p class="val">{cccd}</p>
                        
                        <h3>Chuyến Tàu / Train</h3>
                        <p class="val">{ten_chuyen}</p>
                        
                        <h3>Khoang / Class</h3>
                        <p class="val" style="margin-bottom: 0;">{loai_khoang}</p>
                    </div>
                    <div class="info-right">
                        <h3>Ngày Mua / Date</h3>
                        <p style="font-size: 14px; color: #2c3e50; font-weight: bold; margin-top: 0; margin-bottom: 15px;">{ngay_dat}</p>
                        
                        <h3>Thanh Toán Bằng</h3>
                        <div class="payment-box">{hinh_thuc_tt}</div>
                        
                        <h3 style="margin-top: 5px;">Vị Trí Ghế / Seat</h3>
                        <div class="seat-box">{so_ghe}</div>
                        
                        {qr_html}
                    </div>
                </div>
                <div class="footer">
                    Quý khách có thể chụp ảnh màn hình hoặc in file này để xuất trình khi lên tàu. Xin cảm ơn!
                </div>
            </div>
            <script> window.onload = function() {{ window.print(); }} </script>
        </body>
        </html>
        """
        with open(ten_file, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        os.startfile(ten_file)