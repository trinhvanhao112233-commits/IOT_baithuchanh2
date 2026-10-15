import pika

def callback(ch, method, properties, body):
    print(f"[critical_queue] Da nhan: {body.decode('utf-8')}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')
    channel.queue_declare(queue='critical_queue')
    
    # Bind queue này vào exchange với routing_key là 'critical'
    # Các tin nhắn 'info' hoặc 'warning' sẽ không bao giờ chạy vào queue này
    channel.queue_bind(exchange='iot_alert_exchange', queue='critical_queue', routing_key='critical')

    print('Đang chờ cảnh báo CRITICAL... Nhấn Ctrl+C để thoát.')
    channel.basic_consume(queue='critical_queue', on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    finally:
        connection.close()

if __name__ == '__main__':
    main()