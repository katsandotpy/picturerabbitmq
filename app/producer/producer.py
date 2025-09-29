import pika
import time
import base64

#закодировать картинку в base64, передать в очередь rabbitmq, на контейнере с nginx запустить сайт на котором будет эта картинка
import base64

def image_to_base64(file_path):
    """
    Кодирует изображение в base64 из файла
    """
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


file_path = r"cat.jpg" 
base64_string = image_to_base64(file_path)
print(base64_string[:100] + "...") 



url_params = pika.URLParameters('amqp://rabbit_mq?connection_attempts=10&retry_delay=10')

connection = pika.BlockingConnection(url_params)

channel = connection.channel()

exchange_name = 'direct_logs'
exchange_type = 'direct'

channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

queue_name = 'my_queue'

channel.queue_declare(queue=queue_name)

routing_key = 'info'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

counter = 1
try:
    while True:
        message = base64_string
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
        print(f"Sent: '{message}' with routing key '{routing_key}'")
        counter += 1
        time.sleep(1)  
except KeyboardInterrupt:
    print("\n  aaa...")
finally:
    channel.close()
    connection.close()