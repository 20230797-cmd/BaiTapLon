-- Chỉ định sử dụng đúng Database của bạn
USE QuanLyTauHoa_MSSQL;
GO

-- 1. Tạo bảng Users mới
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,       -- ID tự động tăng
    Username NVARCHAR(50) NOT NULL UNIQUE,      -- Tên đăng nhập (không được trùng)
    Password NVARCHAR(255) NOT NULL,            -- Mật khẩu
    FullName NVARCHAR(100) NOT NULL,            -- Họ và tên
    Phone NVARCHAR(20),                         -- Số điện thoại
    Role NVARCHAR(20) DEFAULT 'User',           -- Quyền: Admin, Staff, User
    CreatedBy INT NULL,                         -- ID của người tạo tài khoản này
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
);
GO

-- 2. Tạo sẵn tài khoản Admin gốc (admin / 123456) để bạn đăng nhập
INSERT INTO Users (Username, Password, FullName, Phone, Role)
VALUES ('admin', '123456', N'Quản Trị Viên Hệ Thống', '0999999999', 'Admin');
GO