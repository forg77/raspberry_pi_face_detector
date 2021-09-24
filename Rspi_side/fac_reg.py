# combined with _reg and _get
# being set at rpi
# send pics to server for each one detected (30 pics per person)
# receive yml file per period
# due to X11 problems in docker ,cv2 window was banned but can be used outside a container
#
import cv2
import numpy as np
import os
import socket
import pickle
import time
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
path="/usr/local/share/opencv4/haarcascades/"
cascadePath = path+"haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
# names = ['None', 'A', 'B', 'C', 'D', 'E'] ...etc can be updated

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)


while True:
    ip_addr = ("10.16.23.122", 9990) 
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
        elif confidence>100:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        face_detector = cv2.CascadeClassifier(path + 'haarcascade_frontalface_default.xml')

        # For each person, enter one numeric face id
        # face_id = input('\n enter user id end press <return> ==>  ')

        # print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0
        face_id = id
        # take face pics
        print(id)
        if id == "unknown" :
            continue

        while True:
            ret, img = cam.read()
            img = cv2.flip(img, -1)  # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
               # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                filename = "dataset/User." + str(face_id) + '.' + str(count) + ".jpg"
                cv2.imwrite(filename, gray[y:y + h, x:x + w])
                os.system("./Encryption ", filename)

                client.send(filename.encode('utf-8'))
                with open(filename, "rb") as ff:
                    data = ff.read()
                    client.sendall(data)
                os.system("./Decryption ", filename)

                # socket to server

                # cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        # print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        # cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        # cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # print(id, " was just detected")

    # cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting
    if k == 27:
        break


# sent to server 30 pics per detect  30*(about 15kb) -> 450kb named User_id.count.jpg
    now_t = int(time.time())
    if now_t % 1500 == 0:
        client.close()
        ip_addr = ("0.0.0.0", 8888)  

        server = socket.socket()
        server.bind(ip_addr)
        server.listen(5)  

        while True: 
            try:
                conn, addr = server.accept()
                file_msg = conn.recv(20480) 

                msg_data = json.loads(file_msg.decode('utf-8'))  

                if msg_data.get("action") == "put":  
                    file_name = msg_data.get("name")
                    file_size = msg_data.get("size")
                    recv_size = 0
                    with open(file_name, "wb") as f:
                        while recv_size != file_size:
                            data = conn.recv(20480)
                            f.write(data)
                            recv_size += len(data)
                    break
            except:
                pass
            server.close()


    client.close()



