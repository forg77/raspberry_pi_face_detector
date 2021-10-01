# raspberry_pi_face_detector_with docker
在docker上运行的树莓派人脸识别程序  
人脸识别的部分用的是这位大佬的代码 https://github.com/Mjrovai/OpenCV-Face-Recognition 致上感谢   
容器环境使用的是这位大佬的镜像  https://github.com/armindocachada/raspberrypi-docker-tensorflow-opencv 致上感谢   
我整合了一下 加上了json和socket用来传送照片和训练成果  
服务器端定时训练后把训练出的yml发回到树莓派  
x11和docker相冲突，仅输出识别出的人名/ID，可以根据需求修改  
整合出的镜像 包含人脸识别、温湿度的内容  直接pull frog77/fg77:v3就可以  

 
  --------------------------------------------------------------------------------------------------------
a face detector can be used in docker container  
Many thanks to @Mjrovai for his https://github.com/Mjrovai/OpenCV-Face-Recognition  
Many thanks to @armindocachada for his https://github.com/armindocachada/raspberrypi-docker-tensorflow-opencv  
DUE TO LIMITATIONS WHEN USING X11 IN DOCKER , ONLY NAME OR ID OF THE DETECTED PERSON CAN BE SHOWN.  
THERE ARE ALSO SOME METHODS CAN SOLVE THIS ,I WOULD LOAD UP IF POSSIBLE.   

if you want to use my image,just pull frog77/fg77:v3 which contains functions such as face recognization and temperature/humidity detection  






