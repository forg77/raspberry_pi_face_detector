import cv2
import numpy as np
from PIL import Image
import os
import pickle
import socket
import struct
import json
import time

# Path for face image database
path = '/home/lvyibin/dataset'
path1 = '/home/lvyibin/anaconda3/lib/python3.6/site-packages/cv2/data/'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(path1 + "haarcascade_frontalface_default.xml")
addr = "0.0.0.0"
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])

        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids


def main():
    bool = 1    # bool值用来翻转客户端和服务端
    count = 0
    while True:
        if bool == 0 && addr != "0.0.0.0":    # 客户端
            print('waiting...')
            ip_addr = (addr, 8888)    # 两台电脑互换地址
            client = socket.socket()
            client.connect(ip_addr)
            faces, ids = getImagesAndLabels(path)
            recognizer.train(faces, np.array(ids))
            # Save the model into trainer/trainer.yml
            recognizer.write('trainer/trainer.yml')
            os.system("python3 Encryption.py trainer/trainer.yml")
            def file_put(filedir):
                if os.path.isfile(filedir):
                    file_name = filedir  # 指定文件名称
                    filenm="trainer.yml"
                    file_size = os.stat(file_name).st_size  # 计算文件大小
                    file_msg = {"action": "put", "name": file_name, "size": file_size}  # 构建一个json文件
                    client.send(bytes(json.dumps(file_msg), encoding="utf-8"))  # 发送传输需要的数据
                    print("文件名: %s --> 文件大小: %s " % (file_name, file_size))
                    with open(file_name, "rb") as f:
                        for line in f:
                            client.send(line)
                            print("文件已发送: %s" % len(line))
                        print("文件发送完成...")

            file_put("trainer/trainer.yml")
            os.system("python3 Decryption.py trainer/trainer.yml")

        elif bool == 1:    # 服务端
            new_t = int(time.time())
            if new_t % 60 == 0:
                bool = 0
                continue
            print('began listening...')
            ip_addr = ("0.0.0.0", 9990)

            server = socket.socket()
            server.bind(ip_addr)
            server.listen(5)
            
            while True:
                try:
                    new_t = int(time.time())
                    if new_t % 60 == 0:
                        bool = 0
                        break
                    conn, addr = server.accept()
                    file_msg = conn.recv(1024)
                    msg_data = json.loads(file_msg.decode('utf-8'))

                    if msg_data.get("action") == "put":  # 是PUT则执行上传
                        file_name = msg_data.get("name")
                        file_size = msg_data.get("size")
                        recv_size = 0
                        file_name = "dataset/" + file_name
                        with open(file_name, "wb") as f:
                            while recv_size != file_size:
                                data = conn.recv(1024)
                                f.write(data)
                                recv_size += len(data)
                                print("文件大小: %s 传输大小: %s" % (file_size, recv_size))
                            print("文件 %s 传输成功..." % file_size)
                        os.system(str("python3 Decryption.py "+file_name))
                        break

                except:
                    pass
            new_t=int(time.time())
            if new_t%60 == 0:
                bool=0
               

if __name__ == '__main__':
    main()
