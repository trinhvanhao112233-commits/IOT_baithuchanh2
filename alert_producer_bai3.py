import pika
import time
import random

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # 1. KHAI BÁO EXCHANGE thay vì Queue
    # - exchange_type='direct': Loại exchange định tuyến chính xác. 
    # Nó sẽ gửi tin nhắn đến các queue có routing_key khớp 100% với routing_key của tin nhắn.
    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')

    # Danh sách các sự kiện mô phỏng (gồm routing_key và nội dung)
    alerts = [
        ('info', 'He thong hoat dong binh thuong'),
        ('warning', 'Nhiet do phong may vuot nguong warning'),
        ('critical', 'Cam bien kho lanh mat ket noi critical')
    ]

    print("Đang phát cảnh báo... Nhấn Ctrl+C để dừng.")
    try:
        while True:
            # Chọn ngẫu nhiên 1 cảnh báo để phát
            routing_key, message = random.choice(alerts)
            
            # Gửi tin nhắn vào EXCHANGE thay vì Queue.
            # Routing key ở đây sẽ quyết định tin nhắn đi vào queue nào (do các consumer quyết định)
            channel.basic_publish(exchange='iot_alert_exchange', routing_key=routing_key, body=message)
            
            print(f"[x] Đã gửi [{routing_key}]: {message}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nĐã dừng.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()