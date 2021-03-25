# ATOM
I am trying to achieve a robot which has telepresence.
you can control the robot as if you are present in that environment.

The project basically uses image processing (Thanks to MEDIAPIPE) 

So what we intend to make is a robotic arm which can mimic the users movement.

Initially, we had to get a good image processing platform. Open CV in python best suits our needs and its flexible too.
Mediapipe was the best choice. It had lots of examples to work with.


![image](https://user-images.githubusercontent.com/57059472/112523878-390a9280-8dc5-11eb-9ac4-e6f2336abd4d.png)


So now, our aim is two process two vedio input at the same time. For the second vedio input i used a IP camera stream. 
But the problem was the dealy after image processing. We are not sure about the reason. 
The delay was finaly avoided after grabing the vedio image by image in jpg format from the ip address. This provided a constant data flow. The images were taken from buffer and decoded using imdecode.

Certain modifications to the initial code was required, but was finaly able to process two vedio sources at the same time.

![image](https://user-images.githubusercontent.com/57059472/112524949-64da4800-8dc6-11eb-96cf-6e1cc856a016.png)


