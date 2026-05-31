<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Hệ Thống Bán Vé Tàu</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">
    <nav class="d-flex justify-content-between align-items-center mb-4 p-3 bg-dark text-white rounded">
        <h2 class="m-0">🚂 VNR ONLINE</h2>
        <div>
            {% if session.get('user_id') %}
                <span>Chào, <b>{{ session.get('full_name') }}</b></span>
                <a href="/dang-xuat" class="btn btn-outline-light btn-sm ms-2">Đăng xuất</a>
            {% else %}
                <a href="/dang-nhap" class="btn btn-warning btn-sm">Đăng nhập</a>
            {% endif %}
        </div>
    </nav>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for cat, msg in messages %}
                <div class="alert alert-{{ cat }}">{{ msg }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <h3>Danh sách chuyến tàu khởi hành</h3>
    <table class="table table-hover mt-3 shadow-sm">
        <thead class="table-primary">
            <tr>
                <th>Mã</th><th>Tên Tàu</th><th>Ga Đi</th><th>Ga Đến</th><th>Ngày</th><th>Thao Tác</th>
            </tr>
        </thead>
        <tbody>
            {% for c in ds_chuyen %}
            <tr>
                <td><b>{{ c[0] }}</b></td>
                <td>{{ c[1] }}</td>
                <td>{{ c[2] }}</td>
                <td>{{ c[3] }}</td>
                <td>{{ c[4] }}</td>
                <td>
                    {% if session.get('user_id') %}
                        <a href="{{ url_for('chon_ghe', ma_chuyen=c[0]) }}" class="btn btn-primary btn-sm">Chọn Ghế</a>
                    {% else %}
                        <a href="/dang-nhap" class="btn btn-outline-secondary btn-sm">Đăng nhập để đặt</a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>