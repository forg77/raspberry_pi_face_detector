import socket
import os
import json
import cv2
import numpy as np
import pickle
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
path = "/usr/local/share/opencv4/haarcascades/"
cascadePath = path + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height
addr = "0.0.0.0"
# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
def main():
    bool = 0    # bool值用来定义处于发送状态还是接收状态，这里是先发送
    count = 0    # 用于计数命名文件
    
    while True:
        if bool == 0:    # 客户端
            def file_put(filedir,filenm):
                if os.path.isfile(filedir):
                    file_name = filedir  # 指定文件名称
               
                    file_size = os.stat(file_name).st_size  # 计算文件大小
                    file_msg = {"action": "put", "name": filenm, "size": file_size}  # 构建一个json文件
                    client.send(bytes(json.dumps(file_msg), encoding="utf-8"))  # 发送传输需要的数据
                    print("文件名: %s --> 文件大小: %s " % (file_name, file_size))
                    with open(file_name, "rb") as f:
                        for line in f:
                            client.send(line)
                            print("文件已发送: %s" % len(line))
                        print("文件发送完成...")
                
            #--------------------------------------------------------------------------------------
            
            print('waiting for file...')
            ip_addr = ("10.16.23.122", 9990)    # 客户端绑定另一个电脑的ipv4地址，端口可换1024到50000以内的值
            client = socket.socket()
            client.connect(ip_addr)
            ret, img = cam.read()
            img = cv2.flip(img, -1)  # Flip vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 50):
                    #  id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                elif confidence > 100:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                face_detector = cv2.CascadeClassifier(path + 'haarcascade_frontalface_default.xml')

                # For each person, enter one numeric face id
                # face_id = input('\n enter user id end press <return> ==>  ')

                # print("\n [INFO] Initializing face capture. Look the camera and wait ...")
                # Initialize individual sampling face count
                countp = 0
                face_id = id
                # take face pics
                print(id)

                if id == "unknown":
                    continue

                ret, img = cam.read()
                img = cv2.flip(img, -1)  # flip video image vertically
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    countp += 1

                    # Save the captured image into the datasets folder
                    filename0 = "/bin/face_rg_dc/face_recognize/dataset/User." + str(face_id) + '.' + str(
                        countp) + ".jpg"
                    cv2.imwrite(filename0, gray[y:y + h, x:x + w])
                    os.system(str("./Encryption " + filename0))
                    filename = str("User." + str(face_id) + '.' + str(countp) + ".jpg")
                    print(filename)
                    file_put(filename0,filename)
                    os.system(str("./Decryption " + filename0))
                    if countp==30 :
                        break
            
                    if os.path.exists('state%s.json' % count):    # 检测当前文件夹下是否存在该文件
                        file_put('state%s.json' % count)  # 调用函数,传输文件
                        count += 1
                        bool = 1
                    else:
                        time.sleep(1)    # 如果文件不存在，等1s进行下次检测
            new_t=int(time.time())
            if new_t%60 == 0:
                bool = 1
                break
        elif bool == 1:    # 服务端
            print('listening...')
            ip_addr = ("0.0.0.0", 8888)    # 绑定本地ipv4地址

            server = socket.socket()
            server.bind(ip_addr)
            server.listen(5)    # 连接队列长度，不用管

            while True:    # 尝试接收，如果失败则重试
                try:
                    conn, addr = server.accept()
                    file_msg = conn.recv(20480)    # 这个长度可以改为1024，和下面同时改

                    msg_data = json.loads(file_msg.decode('utf-8'))    # 注意编解码方式相同
                    filename0="trainer/trainer.yml"
                    if msg_data.get("action") == "put":  # 是PUT则执行上传
                        file_name = msg_data.get("name")
                        file_size = msg_data.get("size")
                        recv_size = 0
                        with open(filename0, "wb") as f:
                            while recv_size != file_size:
                                data = conn.recv(20480)
                                f.write(data)
                                recv_size += len(data)
                                print("文件大小: %s 传输大小: %s" % (file_size, recv_size))
                            print("文件 %s 传输成功..." % file_size)
                        

                        break

                except:
                    pass                
                    break
            os.system("./Decyption trainer/trainer.yml")
            recognizer.read('trainer/trainer.yml')
                
                
if __name__ == '__main__':
    main()
