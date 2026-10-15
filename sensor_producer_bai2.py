import pika
import json
import time
import random
from datetime import datetime

def main():
    # Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # Khai báo queue
    channel.queue_declare(queue='sensor_data_queue')

    # Danh sách các cảm biến mô phỏng
    sensors = ["sensor01", "sensor02", "sensor03"]

    print("Đang mô phỏng gửi dữ liệu cảm biến. Nhấn Ctrl+C để dừng...")
    
    try:
        while True:
            # Sinh dữ liệu ngẫu nhiên
            device_id = random.choice(sensors)
            temperature = round(random.uniform(25.0, 40.0), 1) # Sinh nhiệt độ từ 25.0 đến 40.0
            humidity = round(random.uniform(30.0, 70.0), 1)    # Sinh độ ẩm từ 30.0 đến 70.0
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Tạo payload JSON
            data = {
                "device_id": device_id,
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": timestamp
            }
            payload = json.dumps(data)

            # Gửi dữ liệu vào queue
            channel.basic_publish(
                exchange='',
                routing_key='sensor_data_queue',
                body=payload
            )

            print(f"[x] Đã gửi: {payload}")
            
            # Dừng 3 giây trước khi gửi tiếp
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nĐã dừng gửi dữ liệu.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()