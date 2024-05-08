import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import hashlib
import base64
import json
import random
from typing import Tuple

class OCR:
    @staticmethod
    def make_body_and_sign(image_base64: str) -> Tuple[str, str]:
        body_obj = {
            "images": [
                {
                    "data": image_base64,
                    "dataId": "1",
                    "type": 2
                }
            ],
            "nonce": random.randint(0, 1e5),
            "secretId": "Inner_40731a6efece4c2e992c0d670222e6da",
            "timestamp": int(time.time() * 1000)
        }
        body = json.dumps(body_obj)
        text = body + '43e7a66431b14c8f856a8e889070c19b'
        sign = hashlib.md5(text.encode('utf-8')).hexdigest()
        print("sign: ", sign)
        return body, sign

    @staticmethod
    def get_result(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        body, sign = OCR.make_body_and_sign(encoded_string)
        headers = {
            'CX-Signature': sign,
            'Content-Type': 'application/json;charset=utf-8'
        }
        # print("Body:", body)
        res = requests.post('http://ai.chaoxing.com/api/v1/ocr/common/sync', data=body, headers=headers)
        print("Status Code:", res.status_code)  # 打印状态码
        print("--------------------------------------识别结果如下-------------------------------------------")
        print("Response Body:", res.text)  # 打印响应内容
        try:
            data = res.json()
            result = '\n'.join(i['text'] for i in data['data'][0])
            return result
        except Exception as e:
            print("Error while parsing response:", e)
            return ""

class FileChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.png'):
            time.sleep(1)  # 等待文件完全写入
            result = OCR.get_result(event.src_path)
            print(result)

def monitor_folder(folder: str):
    observer = Observer()
    event_handler = FileChangeHandler()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(3)  # 每秒检查一次
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# 改为自己的文件夹路径
folder = 'C:/Users/86180/Desktop/BigFolder/Screenshots'
monitor_folder(folder)