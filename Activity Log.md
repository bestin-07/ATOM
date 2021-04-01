# Method of apporoach
We will now detail the proposed method of completing the project

**We have mainly two parts. A virtual reality display and Robotic control**

## Virtual reality display ##
For VR display, the Camera used to capture the feed from the robot ( *robot cam* ) is made to rest on a dual axis motor mount. This feed is streamed live through an ip to the application programs.Any normal phone can be mounted on the google cardboard and used. The phone which is kept inside the google cardboard has inbuilt IMU sensors. An android application is used to exploit these features for controlling the dual axis mount of the robot cam to make it act as a virtual reality display.
The camera mount is synced with the values of IMUs in the mobile phone inside the VR headset. When the user moves his head, the corresponding change in IMU values are transferred to the dual axis camera mount in the robot which inturn moves the mount accordingly to match the movement made by the user's head. This will give an immersive experience of observing through the eyes of the robot.

## Robot Control ##
The video to be processed is captured using the back camera of the mobile phone used in the VR headset.It is positioned to capture the arm of the user. The image is set to same aspect ratio as that of *robot cam*. The video from the mobile phone is captured and processed to detect hand of the user. These coordinates compared with the position of robot hand from the *robot cam* and calibrated on every frame. Thus we can achieve a mimicking motion of the users arm hand from the robot arm.

we intent to use raspberry pi 4 for the image processing and arduino for robot control.

![image](https://user-images.githubusercontent.com/57059472/113100125-987aff00-9218-11eb-97cd-1f1705d5130d.png)


Initially, we had to get a good image processing platform. Open CV in python best suits our needs and its flexible too.
Mediapipe was the best choice. It had lots of examples to work with.


![image](https://user-images.githubusercontent.com/57059472/112523878-390a9280-8dc5-11eb-9ac4-e6f2336abd4d.png)



So now, our aim is two process two vedio input at the same time. For the second vedio input i used a IP camera stream. 
But the problem was the dealy after image processing. We are not sure about the reason. 
The delay was finaly avoided after grabing the vedio image by image in jpg format from the ip address. This provided a constant data flow. The images were taken from buffer and decoded using imdecode.

Certain modifications to the initial code was required, but was finaly able to process two vedio sources at the same time.

![image](https://user-images.githubusercontent.com/57059472/112524949-64da4800-8dc6-11eb-96cf-6e1cc856a016.png)


So now, the problems we face is the distance of users hand from the camera. Our current solution is to track a refrence sphere which the user holds and measure is radius. as the radius decreases, the distance in the z axis increases.



![image](https://user-images.githubusercontent.com/57059472/113101016-d0367680-9219-11eb-82d5-1280ad60f1ea.png)