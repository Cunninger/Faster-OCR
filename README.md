## 识别速度快，精度高
>  原理是利用windows自带的截图功能 和 截图默认存储路径，检测文件夹的改变，识别最新截图


## 代码末尾修改
```
# 改为自己的截图文件夹默认存储路径
folder = 'C:/Users/86180/Desktop/BigFolder/Screenshots'
```

## 打包为.exe文件
```
pip install pyinstaller
pyinstaller --onefile monitor_and_ocr.py
```

## 效果
![image](https://github.com/Cunninger/Monitor-OCR/assets/113076850/853c6f83-0a57-4bfb-adf4-84f0cd8ba21c)

## 求个star
![image](https://github.com/Cunninger/Faster-OCR/assets/113076850/9a8b8c14-0ea4-4da4-a302-89a800161b9f)


