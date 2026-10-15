import pika

def callback(ch, method, properties, body):
    print(f"[warning_queue] Da nhan: {body.decode('utf-8')}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # Khai báo exchange giống bên Producer để đảm bảo nó tồn tại
    channel.exchange_declare(exchange='iot_alert_exchange', exchange_type='direct')
    
    # Tạo một queue riêng cho loại cảnh báo này
    channel.queue_declare(queue='warning_queue')
    
    # QUAN TRỌNG: Gắn (Bind) queue này vào exchange với routing_key là 'warning'
    # Bất kỳ tin nào ném vào iot_alert_exchange có routing_key='warning' sẽ lọt vào queue này
    channel.queue_bind(exchange='iot_alert_exchange', queue='warning_queue', routing_key='warning')

    print('Đang chờ cảnh báo WARNING... Nhấn Ctrl+C để thoát.')
    channel.basic_consume(queue='warning_queue', on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    finally:
        connection.close()

if __name__ == '__main__':
    main()