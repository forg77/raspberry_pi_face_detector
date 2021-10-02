import cv2
import numpy as np
import os
from PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = cv2.data.haarcascades+"haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
minW = 64
minH = 64
counta = 0
countc = 0
path = "dataset"
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
path1 = "/home/lvyibin/anaconda3/lib/python3.6/site-packages/cv2/data/"
detector = cv2.CascadeClassifier(path1+'haarcascade_frontalface_default.xml')
for path1 in imagePaths:
    counta = counta + 1
    img = cv2.imread(path1)
    img_numpy = np.array(img, 'uint8')
    idc = int(os.path.split(path1)[-1].split(".")[1])
    faces = detector.detectMultiScale(img_numpy)
    #img_numpy = cv2.flip(img_numpy, -1)  # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if confidence < 100:
            
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))



    # Check if confidence is less them 100 ==> "0" is perfect match
    if idc == id:
        countc = countc + 1
print("recall sensitivity is " , (countc/counta)*100 , "%")
# Do a bit of cleanup
