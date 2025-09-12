# API Hello World

Một API đơn giản trả về "hello world" được xây dựng bằng Django.

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```bash
python manage.py runserver
```

API sẽ chạy tại: `http://localhost:3000`

## API Endpoints

- `GET /api/hello` - Trả về "hello world"
- `GET /api/health` - Kiểm tra trạng thái API

## Ví dụ sử dụng

### Lấy hello world
```bash
curl http://localhost:8000/api/hello
```

Response:
```json
{
  "message": "hello world"
}
```
