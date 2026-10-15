import pika
from datetime import datetime

# Hàm xử lý (callback) sẽ tự động được gọi mỗi khi có tin nhắn mới chạy về queue
def callback(ch, method, properties, body):
    # Lấy giờ hiện tại
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # In ra nội dung tin nhắn (phải decode từ byte sang string)
    print(f"Da nhan message: {body.decode('utf-8')}")
    print(f"Thoi gian nhan: {current_time}")
    print("-" * 30) # Gạch ngang cho dễ nhìn

def main():
    # 1. Kết nối tới RabbitMQ broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # 2. Khai báo lại queue để chắc chắn nó tồn tại (phòng trường hợp chạy Consumer trước Producer)
    channel.queue_declare(queue='iot_lab_queue')
    
    print('Đang chờ message... Nhấn Ctrl+C để thoát.')
    
    # 3. Đăng ký hàm nhận tin nhắn (Consume)
    # - auto_ack=True: Tự động báo cho RabbitMQ biết là đã xử lý xong tin nhắn để xóa khỏi queue.
    channel.basic_consume(queue='iot_lab_queue', on_message_callback=callback, auto_ack=True)

    try:
        # 4. Bắt đầu vòng lặp vô hạn để lắng nghe liên tục
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng Consumer.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()