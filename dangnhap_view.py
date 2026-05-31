<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Sơ đồ ghế - {{ ma_chuyen }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .seat-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
        .seat-item { border: 2px solid #28a745; border-radius: 8px; padding: 15px; cursor: pointer; text-align: center; }
        .btn-check:checked + .seat-item { background-color: #28a745; color: white; }
        .seat-sold { background-color: #e9ecef; border-color: #adb5bd; color: #6c757d; cursor: not-allowed; }
    </style>
</head>
<body class="container py-5 bg-light">
    <div class="card shadow p-4" style="max-width: 800px; margin: auto;">
        <h2 class="text-center text-primary mb-4">CHUYẾN TÀU: {{ ten_chuyen }}</h2>
        <div class="alert alert-info text-center">Vui lòng chọn một ghế trống bên dưới</div>
        
        <form action="/xac-nhan-dat-ve" method="POST">
    <input type="hidden" name="ma_chuyen" value="{{ ma_chuyen }}">
    
    <div class="seat-grid">
    {% if danh_sach_ghe %}
        {% for ghe in danh_sach_ghe %}
            {% if ghe[3] == 'Đã đặt' %}
                <div class="seat-item seat-sold">
                    <b class="d-block">{{ ghe[0] }}</b>
                    <small>{{ ghe[1] }}</small><br>
                    <small class="text-muted">Hết chỗ</small>
                </div>
            {% else %}
                <div class="position-relative">
                    <input type="checkbox" name="danh_sach_ma_ghe" value="{{ ghe[0] }}" id="id_{{ ghe[0] }}" class="btn-check">
                    <label class="seat-item d-block" for="id_{{ ghe[0] }}">
                        <b class="d-block text-primary">{{ ghe[0] }}</b> <div class="small fw-bold text-dark">{{ ghe[1] }}</div> <div class="text-danger fw-bold">{{ "{:,}".format(ghe[2]) }}đ</div> </label>
                </div>
            {% endif %}
        {% endfor %}
    {% else %}
        <div class="alert alert-warning w-100">Chưa có dữ liệu ghế cho chuyến này.</div>
    {% endif %}
</div>

    <button type="submit" class="btn btn-success btn-lg w-100 mt-5 shadow">XÁC NHẬN ĐẶT CÁC GHẾ ĐÃ CHỌN</button>
</form>
    </div>
    <div class="mt-4 p-3 bg-white border rounded shadow-sm">
    <h5 class="m-0">Số ghế đã chọn: <span id="count" class="text-primary">0</span></h5>
    <h4 class="mt-2">Tổng tiền: <span id="total" class="text-danger">0</span> VNĐ</h4>
</div>

<script>
    const checkboxes = document.querySelectorAll('.btn-check');
    const totalDisplay = document.getElementById('total');
    const countDisplay = document.getElementById('count');

    checkboxes.forEach(box => {
        box.addEventListener('change', () => {
            let total = 0;
            let count = 0;
            checkboxes.forEach(cb => {
                if (cb.checked) {
                    // Lấy giá tiền từ thẻ label tương ứng (loại bỏ dấu phẩy và chữ đ)
                    let priceText = cb.nextElementSibling.querySelector('.text-danger').innerText;
                    let price = parseInt(priceText.replace(/[^0-9]/g, ''));
                    total += price;
                    count++;
                }
            });
            totalDisplay.innerText = total.toLocaleString('vi-VN');
            countDisplay.innerText = count;
        });
    });
</script>

</body>
</html>