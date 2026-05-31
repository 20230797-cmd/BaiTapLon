<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng Ký Thành Viên - Tàu Hỏa VN</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background-color: #f4f6f9; }
        .register-container { max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .logo-text { color: #2980b9; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>

<div class="container">
    <div class="register-container">
        <h2 class="logo-text">🚂 ĐĂNG KÝ HÀNH KHÁCH</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} text-center">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form action="/dang-ky" method="POST">
            <div class="mb-3">
                <label class="form-label fw-bold">Tên đăng nhập (*)</label>
                <input type="text" name="username" class="form-control" placeholder="Ví dụ: nguyenvana123" required>
            </div>
            
            <div class="mb-3">
                <label class="form-label fw-bold">Mật khẩu (*)</label>
                <input type="password" name="password" class="form-control" placeholder="Nhập mật khẩu an toàn..." required>
            </div>

            <div class="mb-3">
                <label class="form-label fw-bold">Họ và Tên (*)</label>
                <input type="text" name="fullname" class="form-control" placeholder="Nhập đúng tên trên CCCD..." required>
            </div>

            <div class="mb-3">
                <label class="form-label fw-bold">Số điện thoại</label>
                <input type="tel" name="phone" class="form-control" placeholder="Dùng để nhận thông báo vé...">
            </div>

            <div class="d-grid gap-2 mt-4">
                <button type="submit" class="btn btn-success btn-lg fw-bold">TẠO TÀI KHOẢN NGAY</button>
                <a href="/" class="btn btn-outline-secondary">Quay lại Trang chủ</a>
            </div>
        </form>
    </div>
</div>

</body>
</html>