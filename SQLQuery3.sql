USE QuanLyTauHoa_MSSQL;
GO

-- 1. Tạo bảng Quản lý Ghế Ngồi
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'GheNgoi')
BEGIN
    CREATE TABLE GheNgoi (
        MaGhe VARCHAR(20) PRIMARY KEY,      
        MaChuyen VARCHAR(50) NOT NULL,
        LoaiGhe NVARCHAR(50),               
        GiaVe INT,                          
        TrangThai NVARCHAR(20) DEFAULT N'Trống', 
        FOREIGN KEY (MaChuyen) REFERENCES ChuyenTau(MaChuyen)
    );
END
GO

-- 2. Thêm chuyến tàu mẫu SE1 (nếu chưa có) để Test
IF NOT EXISTS (SELECT * FROM ChuyenTau WHERE MaChuyen = 'SE1')
BEGIN
    INSERT INTO ChuyenTau (MaChuyen, TenChuyen, GaDi, GaDen, NgayDi, GioDi)
    VALUES ('SE1', N'Tàu Thống Nhất', N'Hà Nội', N'Sài Gòn', '2026-06-01', '19:30');
END
GO

-- 3. Thêm ghế mẫu cho chuyến SE1
IF NOT EXISTS (SELECT * FROM GheNgoi WHERE MaGhe = 'K1-01')
BEGIN
    INSERT INTO GheNgoi (MaGhe, MaChuyen, LoaiGhe, GiaVe, TrangThai) VALUES 
    ('K1-01', 'SE1', N'Ngồi Mềm Điều Hòa', 350000, N'Trống'),
    ('K1-02', 'SE1', N'Ngồi Mềm Điều Hòa', 350000, N'Trống'),
    ('K2-01', 'SE1', N'Giường Nằm', 550000, N'Trống');
END
GO