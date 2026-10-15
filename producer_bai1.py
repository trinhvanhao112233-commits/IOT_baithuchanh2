import pika
import time

def main():
    # 1. Tạo kết nối tới RabbitMQ server (broker) đang chạy trên máy cá nhân (localhost)
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    
    # 2. Mở một kênh giao tiếp (channel) bên trong kết nối vừa tạo
    channel = connection.channel()

    # 3. Khai báo hàng đợi (queue) có tên là 'iot_lab_queue'
    # Nếu hàng đợi này chưa có, RabbitMQ sẽ tạo mới. Nếu có rồi thì nó sẽ dùng lại.
    channel.queue_declare(queue='iot_lab_queue')

    # Chuẩn bị nội dung tin nhắn với Mã sinh viên của bạn
    student_info = "Xin chao tu ung dung Python AMQP - b23dccn284 - Trịnh Văn Hào"
    
    print("Đang gửi message... Nhấn Ctrl+C để dừng.")
    try:
        count = 1
        while True: # Vòng lặp vô hạn để gửi liên tục
            # Tạo nội dung tin nhắn đính kèm số đếm
            message = f"{student_info} (Message {count})"
            
            # 4. Gửi tin nhắn (publish message)
            # - exchange='': Dùng mặc định (default exchange), sẽ tự đưa thẳng vào queue có tên trùng với routing_key.
            # - routing_key='iot_lab_queue': Tên của queue đích.
            # - body=message: Nội dung gửi đi.
            channel.basic_publish(exchange='', routing_key='iot_lab_queue', body=message)
            
            print(f"[x] Đã gửi: '{message}'")
            count += 1
            
            # Nghỉ 2 giây trước khi lặp lại gửi tin tiếp theo
            time.sleep(2) 
    except KeyboardInterrupt:
        # Bắt sự kiện người dùng bấm Ctrl+C để thoát
        print("\nĐã dừng Producer.")
    finally:
        # 5. Luôn đóng kết nối an toàn khi chương trình kết thúc
        connection.close()

if __name__ == '__main__':
    main()