import pyodbc
CONNECTION_STRING = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=QuanLyTauHoa_MSSQL;Trusted_Connection=yes;'
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem

class ThongKeView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Tải giao diện Thống Kê
        uic.loadUi('ui/ThongKe.ui', self)
        self.setWindowTitle("Thống Kê Doanh Thu Hệ Thống")
        
        # Cài đặt cột cho Bảng (4 cột)
        self.table_thongke.setColumnCount(4)
        self.table_thongke.setHorizontalHeaderLabels(["Mã Chuyến", "Tên Chuyến", "Số Vé Đã Bán", "Doanh Thu Chuyến (VNĐ)"])
        
        # Gọi hàm tải dữ liệu ngay khi mở
        self.load_data()
        
        # Nút làm mới
        if hasattr(self, 'btn_lammoi'):
            self.btn_lammoi.clicked.connect(self.load_data)

    def load_data(self):
        self.table_thongke.setRowCount(0)
        conn = pyodbc.connect(CONNECTION_STRING)
        
        query = """
            SELECT c.ma_chuyen, c.ten_chuyen, COUNT(v.ma_ve) as so_ve, SUM(v.gia_ve) as doanh_thu
            FROM chuyen_tau c
            LEFT JOIN ve_tau v ON c.ma_chuyen = v.ma_chuyen
            GROUP BY c.ma_chuyen, c.ten_chuyen 
        """
        rows = conn.execute(query).fetchall()
        
        tong_tien_toan_he_thong = 0
        
        for row_idx, row_data in enumerate(rows):
            self.table_thongke.insertRow(row_idx)
            
            ma_chuyen = row_data[0]
            ten_chuyen = row_data[1]
            so_ve = row_data[2]
            # Nếu chuyến tàu chưa bán được vé nào thì SUM = None, ta chuyển thành 0
            doanh_thu = row_data[3] if row_data[3] else 0 
            
            tong_tien_toan_he_thong += doanh_thu
            
            # Định dạng số tiền cho đẹp (VD: 1,500,000 đ)
            doanh_thu_str = "{:,.0f}".format(doanh_thu) + " đ"
            
            # Nhét vào bảng
            self.table_thongke.setItem(row_idx, 0, QTableWidgetItem(str(ma_chuyen)))
            self.table_thongke.setItem(row_idx, 1, QTableWidgetItem(str(ten_chuyen)))
            self.table_thongke.setItem(row_idx, 2, QTableWidgetItem(str(so_ve)))
            self.table_thongke.setItem(row_idx, 3, QTableWidgetItem(doanh_thu_str))
            
        conn.close()
        
        # Cập nhật con số tổng xuống cái nhãn (Label) dưới cùng
        if hasattr(self, 'lbl_tongdoanhthu'):
            tong_str = "{:,.0f}".format(tong_tien_toan_he_thong)
            self.lbl_tongdoanhthu.setText(f"TỔNG DOANH THU HỆ THỐNG: {tong_str} VNĐ")