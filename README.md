# raspberry_pi_face_detector
在docker上运行的树莓派人脸识别程序  
人脸识别的部分用的是这位大佬的代码 https://github.com/Mjrovai/OpenCV-Face-Recognition   
我整合了一下 加上了json和socket用来传送照片和训练成果  
服务器端定时训练后把训练出的yml发回到树莓派  


