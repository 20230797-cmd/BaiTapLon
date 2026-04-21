import sqlite3

def xoa_sach_ve():
    conn = sqlite3.connect('quanlytauhoa.db')
    # Lệnh này sẽ quét sạch toàn bộ vé đã bán, reset doanh thu về 0
    conn.execute("DELETE FROM ve_tau")
    conn.commit()
    conn.close()
    print("Đã xóa sạch lịch sử bán vé! Doanh thu đã về 0.")

if __name__ == '__main__':
    xoa_sach_ve()