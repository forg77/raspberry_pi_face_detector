# to server at 10.16.23.122
# get 5 pics per occurrence * only the known ones
# need to be guided by admin
# send back to rpi per period*

# period* duration is 300s as well can be changed
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
path = '../dataset'
path1 = "/usr/local/share/opencv4/haarcascades/"
detector = cv2.CascadeClassifier(path1 + "haarcascade_frontalface_default.xml");

# function to get the images and label data
nowid = 0


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


while True:
    s = socket.socket()
    iport = (('0.0.0.0', 9990))

    s.bind(iport)
    s.listen(5)
    conn, addr = s.accept()
    # pic rec
    F_name = conn.recv(1024)
    F_name = F_name.decode()
    contain_F = conn.recv(32768)
    f1 = open(F_name, 'wb')
    f1.write(b''.join(contain_F))
    os.system("python3 Decryption ../dataset/", F_name)
    #
    new_t = int(time.time())
    if new_t % 1500 == 0:
        s.close()
        ip_addr = (addr, 9993)
        client = socket.socket()
        client.connect(ip_addr)
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml')
        old_t = new_t
        filedir = 'trainer/trainer.yml'
        os.system("python3 Encryption.py trainer/trainer.yml")
        if os.path.isfile(filedir):
            file_name = filedir  # 指定文件名称
            file_size = os.stat(file_name).st_size  # 计算文件大小
            file_msg = {"action": "put", "name": file_name, "size": file_size}  # 构建一个json文件
            client.send(bytes(json.dumps(file_msg), encoding="utf-8"))  # 发送传输需要的数据
            # print("文件名: %s --> 文件大小: %s " % (file_name, file_size))
            with open(file_name, "rb") as f:
                for line in f:
                    client.send(line)

            # Print the numer of faces trained and end program
        client.close()

        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    s.close()
    # send to rpi per period
    # 1. yml file back
