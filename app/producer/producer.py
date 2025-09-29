import pika
import base64
import requests
from io import BytesIO
from PIL import Image

def resize_and_encode_image(image_url, max_size=(800, 600), quality=85):
    """
    Скачивает изображение, уменьшает его и кодирует в base64
    """
    try:
        # Скачиваем изображение
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Открываем изображение с PIL
        image = Image.open(BytesIO(response.content))
        
        print(f" [x] Original image size: {image.size}")
        
        # Уменьшаем изображение сохраняя пропорции
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        print(f" [x] Resized image size: {image.size}")
        
        # Конвертируем в RGB если нужно (для JPEG)
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Сохраняем в буфер с уменьшенным качеством
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        # Кодируем в base64
        encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return encoded_string
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None

def main():
    # Подключаемся к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    # Создаем очередь
    channel.queue_declare(queue='hello')
    
    # URL изображения из интернета
    image_url = "https://i.pinimg.com/736x/1d/47/c5/1d47c5877fe0ba2481dadf5cf98c1bb0.jpg"
    
    # Обрабатываем и кодируем изображение
    base64_string = resize_and_encode_image(
        image_url, 
        max_size=(800, 600),  # Максимальные размеры
        quality=75            # Качество JPEG (1-100)
    )
    
    if base64_string:
        # Отправляем сообщение
        channel.basic_publish(exchange='', routing_key='hello', body=base64_string)
        print(" [x] Sent resized image data to RabbitMQ")
        print(f" [x] Base64 length: {len(base64_string)} characters")
    else:
        print(" [x] Failed to encode image")
    
    connection.close()

if __name__ == '__main__':
    main()