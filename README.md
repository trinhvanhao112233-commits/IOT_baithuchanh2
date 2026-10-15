# BÁI THỰC HÀNH 2: TÌM HIỂU VÀ LẬP TRÌNH VỚI AMQP (RABBITMQ)

## 1. Thông Tin Chung

| Mục | Nội dung |
| :--- | :--- |
| **Môn học** | Internet of Things (IoT) |
| **Giao thức** | AMQP (Advanced Message Queuing Protocol) |
| **Broker sử dụng** | RabbitMQ Server (`localhost:5672`) |
| **Ngôn ngữ** | Python 3.x (Thư viện: `pika`) |

---

## 2. Cấu Trúc Mã Nguồn

```text
├── producer_bai1.py            # Bài 1: Producer gửi message cơ bản
├── consumer_bai1.py            # Bài 1: Consumer nhận và in message
├── sensor_producer_bai2.py     # Bài 2: Mô phỏng cảm biến IoT gửi telemetry JSON
├── monitor_consumer_bai2.py    # Bài 2: Consumer nhận, kiểm tra ngưỡng và cảnh báo
├── alert_producer_bai3.py      # Bài 3: Producer gửi cảnh báo phân loại qua Direct Exchange
├── warning_consumer_bai3.py    # Bài 3: Consumer lọc nhận cảnh báo mức WARNING
├── critical_consumer_bai3.py   # Bài 3: Consumer lọc nhận cảnh báo mức CRITICAL
└── README.md                   # Hướng dẫn chi tiết bài thực hành
```

---

## 3. Cài Đặt Môi Trường

### Cài đặt thư viện Python:
```bash
pip install pika
```

### Khởi động RabbitMQ Server trên Windows:
- **Cách 1**: Chạy PowerShell bằng quyền Administrator:
  ```powershell
  rabbitmq-service start
  ```
- **Cách 2**: Mở ứng dụng **Services** trong Windows $\rightarrow$ tìm dịch vụ `RabbitMQ` $\rightarrow$ bấm **Start**.

---

## 4. Chi Tiết Các Bài Thực Hành

### BÀI 1: Kết Nối Broker Và Truyền Message Cơ Bản (Queue Trực Tiếp)

#### Mô tả:
- Sử dụng **Default Exchange** (`exchange=''`) gửi tin nhắn trực tiếp vào queue `iot_lab_queue`.
- **Producer**: Gửi thông điệp chứa thông tin sinh viên và số thứ tự message tuần hoàn mỗi 2 giây.
- **Consumer**: Lắng nghe queue, giải mã UTF-8 và in thông điệp kèm mốc thời gian nhận.

#### Cách chạy:
1. Mở Terminal 1 (chạy Consumer):
   ```bash
   python consumer_bai1.py
   ```
2. Mở Terminal 2 (chạy Producer):
   ```bash
   python producer_bai1.py
   ```

#### Kết quả mong đợi:
- **Producer**:
  ```text
  Đang gửi message... Nhấn Ctrl+C để dừng.
  [x] Đã gửi: 'Xin chao tu ung dung Python AMQP - b23dccn284 - Trịnh Văn Hào (Message 1)'
  [x] Đã gửi: 'Xin chao tu ung dung Python AMQP - b23dccn284 - Trịnh Văn Hào (Message 2)'
  ```
- **Consumer**:
  ```text
  Đang chờ message... Nhấn Ctrl+C để thoát.
  Da nhan message: Xin chao tu ung dung Python AMQP - b23dccn284 - Trịnh Văn Hào (Message 1)
  Thoi gian nhan: 20:55:12
  ------------------------------
  Da nhan message: Xin chao tu ung dung Python AMQP - b23dccn284 - Trịnh Văn Hào (Message 2)
  Thoi gian nhan: 20:55:14
  ------------------------------
  ```

---

### BÀI 2: Mô Phỏng Cảm Biến IoT Gửi Dữ Liệu Môi Trường (Telemetry & Cảnh Báo)

#### Mô tả:
- **Queue sử dụng**: `sensor_data_queue`.
- **Sensor Producer**: Mô phỏng nhiều trạm cảm biến (`sensor01`, `sensor02`, `sensor03`), tạo ngẫu nhiên nhiệt độ (25.0 - 40.0°C) và độ ẩm (30.0 - 70.0%), đóng gói JSON kèm `timestamp` gửi mỗi 3 giây.
- **Monitoring Consumer**: Parse dữ liệu JSON, hiển thị thông số và kiểm tra logic cảnh báo:
  - Nếu `temperature > 35` $\rightarrow$ Cảnh báo: `CANH BAO: Nhiet do cao`
  - Nếu `humidity < 40` $\rightarrow$ Cảnh báo: `CANH BAO: Do am thap`

#### Cách chạy:
1. Mở Terminal 1 (chạy Consumer):
   ```bash
   python monitor_consumer_bai2.py
   ```
2. Mở Terminal 2 (chạy Producer):
   ```bash
   python sensor_producer_bai2.py
   ```

#### Kết quả mong đợi:
- **Sensor Producer**:
  ```text
  Đang mô phỏng gửi dữ liệu cảm biến. Nhấn Ctrl+C để dừng...
  [x] Đã gửi: {"device_id": "sensor02", "temperature": 37.8, "humidity": 35.4, "timestamp": "2026-10-15 20:45:10"}
  [x] Đã gửi: {"device_id": "sensor01", "temperature": 27.3, "humidity": 58.2, "timestamp": "2026-10-15 20:45:13"}
  [x] Đã gửi: {"device_id": "sensor03", "temperature": 38.5, "humidity": 62.7, "timestamp": "2026-10-15 20:45:16"}
  ```
- **Monitoring Consumer**:
  ```text
  Đang chờ nhận dữ liệu IoT... Nhấn Ctrl+C để thoát.
  Device: sensor02
  Time: 2026-10-15 20:45:10
  Temperature: 37.8
  Humidity: 35.4
  CANH BAO: Nhiet do cao
  CANH BAO: Do am thap
  ------------------------------
  Device: sensor01
  Time: 2026-10-15 20:45:13
  Temperature: 27.3
  Humidity: 58.2
  ------------------------------
  Device: sensor03
  Time: 2026-10-15 20:45:16
  Temperature: 38.5
  Humidity: 62.7
  CANH BAO: Nhiet do cao
  ------------------------------
  ```

---

### BÀI 3: Định Tuyến Cảnh Báo Với Direct Exchange (Routing Key)

#### Mô tả:
- Khai báo Exchange loại `direct` mang tên `iot_alert_exchange`.
- **Alert Producer**: Phát các cảnh báo hệ thống ngẫu nhiên gắn với các `routing_key`: `info`, `warning`, `critical`.
- **Hệ thống Consumer độc lập theo phân loại**:
  - `warning_consumer_bai3.py`: Khai báo queue `warning_queue` bind với `routing_key='warning'`.
  - `critical_consumer_bai3.py`: Khai báo queue `critical_queue` bind với `routing_key='critical'`.
  - Tin nhắn `info` không được bind sẽ tự động bị bỏ qua, đảm bảo phân tách trách nhiệm xử lý theo mức độ khẩn cấp.

#### Cách chạy:
1. Mở Terminal 1 (chạy Warning Consumer):
   ```bash
   python warning_consumer_bai3.py
   ```
2. Mở Terminal 2 (chạy Critical Consumer):
   ```bash
   python critical_consumer_bai3.py
   ```
3. Mở Terminal 3 (chạy Alert Producer):
   ```bash
   python alert_producer_bai3.py
   ```

#### Kết quả mong đợi:
- **Alert Producer**:
  ```text
  Đang phát cảnh báo... Nhấn Ctrl+C để dừng.
  [x] Đã gửi [warning]: Nhiet do phong may vuot nguong warning
  [x] Đã gửi [info]: He thong hoat dong binh thuong
  [x] Đã gửi [critical]: Cam bien kho lanh mat ket noi critical
  ```
- **Warning Consumer**:
  ```text
  Đang chờ cảnh báo WARNING... Nhấn Ctrl+C để thoát.
  [warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
  ```
- **Critical Consumer**:
  ```text
  Đang chờ cảnh báo CRITICAL... Nhấn Ctrl+C để thoát.
  [critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
  ```
