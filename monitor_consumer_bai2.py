import pika
import json

def callback(ch, method, properties, body):
    # Phân tích dữ liệu JSON nhận được
    data = json.loads(body.decode('utf-8'))
    
    device_id = data.get("device_id")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    timestamp = data.get("timestamp")
    
    # In thông tin theo định dạng yêu cầu
    print(f"Device: {device_id}")
    if timestamp:
        print(f"Time: {timestamp}")
    print(f"Temperature: {temperature}")
    print(f"Humidity: {humidity}")
    
    # Kiểm tra và phát ra cảnh báo
    if temperature > 35:
        print("CANH BAO: Nhiet do cao")
    if humidity < 40:
        print("CANH BAO: Do am thap")
        
    print("-" * 30) # Đường gạch ngang phân cách các lần nhận để dễ nhìn

def main():
    # Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    
    # Đảm bảo queue sensor_data_queue đã tồn tại
    channel.queue_declare(queue='sensor_data_queue')
    
    print('Đang chờ nhận dữ liệu IoT... Nhấn Ctrl+C để thoát.')
    
    # Đăng ký hàm callback xử lý message
    channel.basic_consume(
        queue='sensor_data_queue',
        on_message_callback=callback,
        auto_ack=True
    )
    
    try:
        # Bắt đầu lắng nghe
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng nhận dữ liệu.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()