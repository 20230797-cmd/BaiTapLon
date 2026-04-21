import sqlite3

def sua_gia_ve_hop_li():
    conn = sqlite3.connect('quanlytauhoa.db')
    
    # 1. Reset toàn bộ các vé đang có giá "trên trời" (lớn hơn 2 triệu) về mức 150.000đ
    conn.execute("UPDATE ve_tau SET gia_ve = 150000 WHERE gia_ve > 2000000")
    
    # 2. Cập nhật giá theo khoảng cách (Ví dụ dựa vào mã chuyến của bạn)
    # Tuyến ngắn (VD: Hà Nội - Thanh Hóa, Vinh...)
    conn.execute("UPDATE ve_tau SET gia_ve = 150000 WHERE ma_chuyen = '01'") 
    
    # Tuyến vừa (VD: Hà Nội - Quảng Bình như trong ảnh của bạn)
    conn.execute("UPDATE ve_tau SET gia_ve = 250000 WHERE ma_chuyen = '02'")
    
    # Tuyến dài (VD: Hà Nội - Đà Nẵng, Sài Gòn...)
    conn.execute("UPDATE ve_tau SET gia_ve = 500000 WHERE ma_chuyen = '03'") 
    
    conn.commit()
    conn.close()
    print("Đã cập nhật lại toàn bộ giá vé về mức hợp lý!")

if __name__ == '__main__':
    sua_gia_ve_hop_li()