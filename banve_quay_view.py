USE QuanLyTauHoa_MSSQL;
GO

-- 1. Nếu bảng ChiTietLoTrinh bị lỗi tạo dở ở lần trước, ta xóa nó đi để làm lại cho sạch
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'ChiTietLoTrinh')
BEGIN
    DROP TABLE ChiTietLoTrinh;
END
GO

-- 2. Tạo lại bảng với kiểu dữ liệu VARCHAR(50) (hoặc bạn có thể tự đổi thành VARCHAR(20) nếu bảng ChuyenTau của bạn dùng kiểu đó)
CREATE TABLE ChiTietLoTrinh (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    MaChuyen VARCHAR(50) NOT NULL,    -- ĐÃ SỬA THÀNH VARCHAR ĐỂ KHỚP VỚI BẢNG GỐC
    TenGa NVARCHAR(100) NOT NULL,
    ThuTuDung INT NOT NULL,           
    ThoiGianDen NVARCHAR(20),         
    ThoiGianDi NVARCHAR(20),          
    GhiChu NVARCHAR(255),
    FOREIGN KEY (MaChuyen) REFERENCES ChuyenTau(MaChuyen) ON DELETE CASCADE
);
GO

-- 3. Thêm thử lộ trình mẫu
BEGIN TRY
    INSERT INTO ChiTietLoTrinh (MaChuyen, TenGa, ThuTuDung, ThoiGianDen, ThoiGianDi) VALUES
    ('SE1', N'Hà Nội', 1, N'Xuất phát', '19:30'),
    ('SE1', N'Thanh Hóa', 2, '22:45', '22:50'),
    ('SE1', N'Vinh', 3, '01:10', '01:15'),
    ('SE1', N'Đà Nẵng', 4, '11:40', '11:55'),
    ('SE1', N'Sài Gòn', 5, '04:10', N'Kết thúc');
END TRY
BEGIN CATCH 
    -- Bỏ qua nếu SE1 không tồn tại
END CATCH
GO


ALTER TABLE VeTau ADD GiaVe INT;



-- 1. Xóa dữ liệu cũ của 5 tàu này (nếu có) để không bị lỗi trùng mã ghế
DELETE FROM GheNgoi WHERE MaChuyen IN ('LP3', 'SE1', 'SE2', 'SPT1', 'TN1');

-- 2. Khai báo danh sách các chuyến tàu
DECLARE @TrainList TABLE (MaChuyen VARCHAR(50));
INSERT INTO @TrainList VALUES ('LP3'), ('SE1'), ('SE2'), ('SPT1'), ('TN1');

DECLARE @CurrentTrain VARCHAR(50);
DECLARE @i INT;
DECLARE @MaGhe VARCHAR(20);
DECLARE @LoaiGhe NVARCHAR(50);
DECLARE @GiaVe INT;

-- 3. Vòng lặp duyệt qua từng chuyến tàu
DECLARE TrainCursor CURSOR FOR SELECT MaChuyen FROM @TrainList;
OPEN TrainCursor;
FETCH NEXT FROM TrainCursor INTO @CurrentTrain;

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @i = 1;
    
    -- Vòng lặp tạo 60 ghế cho chuyến tàu hiện tại
    WHILE @i <= 60
    BEGIN
        -- Tạo mã ghế đẹp (VD: LP3-01, SE1-15, SPT1-60)
        IF @i < 10
            SET @MaGhe = @CurrentTrain + '-0' + CAST(@i AS VARCHAR(2));
        ELSE
            SET @MaGhe = @CurrentTrain + '-' + CAST(@i AS VARCHAR(2));

        -- Phân loại 30 ghế đầu là Ngồi mềm, 30 ghế sau là Giường nằm
        IF @i <= 30
        BEGIN
            SET @LoaiGhe = N'Ngồi Mềm Điều Hòa';
            SET @GiaVe = 350000;
        END
        ELSE
        BEGIN
            SET @LoaiGhe = N'Giường Nằm Khoang 4';
            SET @GiaVe = 650000;
        END

        -- Chèn dữ liệu vào bảng GheNgoi của bạn
        INSERT INTO GheNgoi (MaGhe, MaChuyen, LoaiGhe, GiaVe, TrangThai)
        VALUES (@MaGhe, @CurrentTrain, @LoaiGhe, @GiaVe, N'Trống');

        SET @i = @i + 1;
    END

    FETCH NEXT FROM TrainCursor INTO @CurrentTrain;
END

CLOSE TrainCursor;
DEALLOCATE TrainCursor;

-- In ra thông báo khi hoàn thành
PRINT N'Đã tạo thành công 300 ghế cho 5 chuyến tàu!';
