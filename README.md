# raspberry_pi_face_detector_with docker
在docker上运行的树莓派人脸识别程序  
人脸识别的部分用的是这位大佬的代码 https://github.com/Mjrovai/OpenCV-Face-Recognition 致上感谢   
容器环境使用的是这位大佬的镜像  https://github.com/armindocachada/raspberrypi-docker-tensorflow-opencv 致上感谢   
我整合了一下 加上了json和socket用来传送照片和训练成果  
服务器端定时训练后把训练出的yml发回到树莓派  
x11和docker相冲突，仅输出识别出的人名/ID，可以根据需求修改  
整合出的镜像 包含人脸识别、温湿度的内容  直接pull frog77/fg77:v3就可以  
没有其他特别要求的话可以直接在服务器端和树莓派容器端分别运行server.py 和 client.py  

----------------------------------------------------------------------------------------------
1.需要在其他平台计算出train.yml  
  直接用facetrain.py就可以得出训练结果(train.yml)  这个训练结果大概是通用的  
2.计算召回率
简单介绍一下计算召回率的方法：  
  先用face_get.py获取数据集 然后可以用evualte.py来计算出召回率  
3.各类问题
a.在调试程序的时候经常遇到opencv路径问题，这里留下我常用来查找opencv的方法，或许能让你少走一些弯路  
  sudo find / -iname "*opencv*" > /你希望的位置/opencv_find.txt  
  适应的问题 cv2.cv2 没有face模块 等  
b.有时候会遇到-215问题，实践时主要发现三种可能：  
  a)图片路径问题  
  b)摄像头占用 ps命令查看运行程序 sudo kill -9 ID 终止  
  c)启动容器时加上--privileged 例如 run -itd --privileged 镜像ID 或者 exec -it --privileged 容器ID /bin/bash  
c.遇到端口占用问题 socket errorno98：  
  同上b) lsof -i:端口号 然后 kill -9 ID 删掉进程稍等片刻  
祝好运！但愿不出bug！  
永远要仔细检查文件、库的路径！加油！！！ 


  --------------------------------------------------------------------------------------------------------
a face detector can be used in docker container  
Many thanks to @Mjrovai for his https://github.com/Mjrovai/OpenCV-Face-Recognition  
Many thanks to @armindocachada for his https://github.com/armindocachada/raspberrypi-docker-tensorflow-opencv  
DUE TO LIMITATIONS WHEN USING X11 IN DOCKER , ONLY NAME OR ID OF THE DETECTED PERSON CAN BE SHOWN.  
THERE ARE ALSO SOME METHODS CAN SOLVE THIS ,I WOULD LOAD UP IF POSSIBLE.   

if you want to use my image,just pull frog77/fg77:v3 which contains functions such as face recognition and temperature/humidity detection  
Here is a brief introduction of calculating recall sensitivity:  
run face_get.py to get the dataset then run evualte.py to calculate recall sensitivity  
If you are willing to calculate train.yml at other pcs(or sth else) run facetrain.py and copy train.yml to where you want  

-------------------------------------------------------------------------------------------------------
Some frequently met errors:  
cv2 location related errors: run sudo find / -iname "*opencv*" > /path_you_want/opencv_find.txt and check the txt  
opencv errorno -215:
  check your pic path
  kill other process using your cam: ps to check processes and then sudo kill -9 ID
  run your container with --privileged :such as run -itd --privileged imageID or exec -it --privileged containerID /bin/bash  
address been used (socket errorno98)"
  run lsof -i:portid and kill -9 ID  
 
 
 WISH YOU GOOD LUCK! MAY NO BUGS SHALL BOTHER YOU!
 ALWAYS CHECK FILE PATH CAREFULLY! JIAYOU!!! 







