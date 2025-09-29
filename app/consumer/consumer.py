import pika
import base64
import os
import json
from datetime import datetime

def callback(ch, method, properties, body):
    try:
        print(" [x] Received image data")
        
        # Декодируем base64 обратно в бинарные данные
        image_data = base64.b64decode(body)
        
        # Создаем директорию для изображений, если её нет
        images_dir = "/usr/share/nginx/html/images"
        os.makedirs(images_dir, exist_ok=True)
        
        # Сохраняем изображение
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"received_{timestamp}.jpg"
        image_path = os.path.join(images_dir, image_filename)
        
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)
        
        print(f" [x] Image saved as {image_path}")
        
        # Обновляем HTML страницу
        update_html_page(image_filename)
        
    except Exception as e:
        print(f" [x] Error processing message: {e}")

def update_html_page(image_filename):
    """Создает или обновляет HTML страницу для отображения изображения"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RabbitMQ Image Receiver</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .image-container {{
                text-align: center;
                margin: 20px 0;
            }}
            .image-container img {{
                max-width: 100%;
                max-height: 600px;
                border: 2px solid #ddd;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            .info {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1> Image from RabbitMQ</h1>
            <div class="info">

            </div>
            <div class="image-container">
                <img src="/images/{image_filename}" alt="Received from RabbitMQ">
            </div>
        </div>
    </body>
    </html>
    """
    
    html_path = "/usr/share/nginx/html/index.html"
    with open(html_path, "w") as html_file:
        html_file.write(html_content)
    
    print(f" [x] HTML page updated with image: {image_filename}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()