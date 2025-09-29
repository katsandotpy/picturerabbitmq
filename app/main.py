#закодировать картинку в base64, передать в очередь rabbitmq, на контейнере с nginx запустить сайт на котором будет эта картинка
import base64
import requests
from io import BytesIO

def image_to_base64(image_url):
    """
    Кодирует изображение из URL в base64
    """
    # Скачиваем изображение из интернета
    response = requests.get(image_url)
    response.raise_for_status()  # Проверяем успешность запроса
    
    # Кодируем в base64
    encoded_string = base64.b64encode(response.content).decode('utf-8')
    return encoded_string

# Использование
file_path = "https://i.pinimg.com/736x/1d/47/c5/1d47c5877fe0ba2481dadf5cf98c1bb0.jpg" 
base64_string = image_to_base64(file_path)
print(base64_string[:100] + "...")