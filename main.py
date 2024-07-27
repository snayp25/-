import json
import time
import base64
from io import BytesIO
from PIL import Image
import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]

            attempts -= 1
            time.sleep(delay)
    def base64_img(self , images, path_img):
        # Декодируем строку base64 в байты
        image_bytes = base64.b64decode(images)

        # Открываем изображение с помощью Pillow
        image = Image.open(BytesIO(image_bytes))
        image.show()
        image.save(path_img)

if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '9987ED3717CA963CDB314E972CBF56AD', 'C380681D77C9EB0A8BE5A812615A3668')
    model_id = api.get_model()
    uuid = api.generate("banana", model_id)
    images = api.check_generation(uuid)
    # print(images)

    with open('1.text', 'w') as file:
        file.write(images)

    api.base64_img(images, "test.jpg")