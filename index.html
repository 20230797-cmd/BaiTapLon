-- Chuyển đúng vào Database của bạn
USE QuanLyTauHoa_MSSQL;
GO

-- 1. Tạo bảng Chuyến Tàu
CREATE TABLE ChuyenTau (
    MaChuyen VARCHAR(50) PRIMARY KEY,       -- VD: SE1, TN1...
    TenChuyen NVARCHAR(100) NOT NULL,       -- Tàu Khách Thống Nhất...
    GaDi NVARCHAR(100) NOT NULL,
    GaDen NVARCHAR(100) NOT NULL,
    NgayDi NVARCHAR(20),                    -- Dùng chuỗi cho dễ nhập liệu ban đầu
    GioDi NVARCHAR(20)
);
GO

-- 2. Tạo bảng Ga Tàu
CREATE TABLE GaTau (
    MaGa VARCHAR(50) PRIMARY KEY,
    TenGa NVARCHAR(100) NOT NULL,
    DiaChi NVARCHAR(255)
);
GO

-- 3. Tạo bảng Khách Hàng
CREATE TABLE KhachHang (
    MaKH VARCHAR(50) PRIMARY KEY,
    TenKH NVARCHAR(100) NOT NULL,
    CCCD VARCHAR(20),
    SDT VARCHAR(20)
);
GO

-- 4. Tạo bảng Nhân Viên
CREATE TABLE NhanVien (
    MaNV VARCHAR(50) PRIMARY KEY,
    TenNV NVARCHAR(100) NOT NULL,
    ChucVu NVARCHAR(100),
    SDT VARCHAR(20)
);
GO

-- 5. Tạo bảng Vé Tàu (Liên kết với Chuyến Tàu và Users)
CREATE TABLE VeTau (
    MaVe INT IDENTITY(1,1) PRIMARY KEY,             -- Mã vé tự tăng
    MaChuyen VARCHAR(50),                           -- Cột khóa ngoại
    UserID INT,                                     -- ID Khách hàng đặt vé
    TenHanhKhach NVARCHAR(100) NOT NULL,
    CCCD VARCHAR(20) NOT NULL,
    LoaiGhe NVARCHAR(50),
    NgayDat DATETIME,
    
    -- Tạo ràng buộc khóa ngoại (Rất tốt để báo cáo đồ án)
    FOREIGN KEY (MaChuyen) REFERENCES ChuyenTau(MaChuyen),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO