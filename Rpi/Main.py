
#################################  Initializations  ##################################################
import cv2
import numpy as np
import requests                               

#url = 'http://192.168.0.6:8080/shot.jpg'            # For Ip
cap = cv2.VideoCapture(0)                       # For webcam input

x=y=x1=x2=y1=y2=0                                           
zmem = 30 #For the memory of the previous z value and 30 is an initial z value

############################### Connecting To Arduino ###############################################
import serial
import time
arduino = serial.Serial('COM5', 9600, timeout=0)
time.sleep(2)
######################################################################################################



def communicator(x,xdir,y,ydir):
    import struct
    # send the first int in binary format
    arduino.write(struct.pack('>BBBB',x,xdir,y,ydir))




######################### For calculating the z value from reference sphere ##########################
def zvalue(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 2000, param1 = 100, param2 = 40, minRadius = 5, maxRadius = 120)
    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            z = (((r-39)/8)*-5)+25
            #print(r,' ',z)
            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)
  
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
            return z
    else:
        return zmem
######################################################################################################


############################## Calculating the angle #################################################
def angle_calculator(x,y,z):
    import math
    dirx = diry = 1
    # add a if with contiton that robot spherical ball should be within range of obtained x,y,z for robot logic to work
    xcm = (x * .02171875) - 6.95   #since we take value from half of the sceen. width = 13.9 cm  = .02171875 cm per pixel 
    ycm = (y * .02171875) - 5.4    #since we take value from half of the sceen. height = 10.8 cm  = .02171875 cm per pixel 
    ######## x values
    if z is not None:
        anglex = int(math.degrees(math.atan2(xcm,z)))
    else:
        anglex = int(math.degrees(math.atan2(xcm,30)))    
    if x > 320:
        print('X-RIGHT',' ',anglex," Degrees")       
    else:
        print('X-LEFT',' ',-anglex," Degrees")
        anglex = -anglex
        dirx = 0
    
    ######## y values
    if z is not None:
        angley = int(math.degrees(math.atan2(ycm,z)))
    else:
        angley = int(math.degrees(math.atan2(ycm,30)))    
    if y < 240:
        print('Y-UP',' ',-angley," Degrees")
        angley = -angley       
    else:
        print('Y-DOWN',' ',angley, "Degrees")
        diry = 0


    communicator(anglex,dirx,angley,diry)    
######################################################################################################





######################################### PROCESSING #################################################
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.6,min_tracking_confidence=0.5)

while True:
    success, image = cap.read()
    #img_resp = requests.get(url)
    #img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #image = cv2.imdecode(img_arr, -1)
    #image = cv2.flip(image, 1)
        
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
        
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    height = image.shape[0]
    width = image.shape[1]
    zmem = zvalue(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x1 = int((hand_landmarks.landmark[4].x )* width)
            y1 = int((hand_landmarks.landmark[4].y )* height)
            x2 = int((hand_landmarks.landmark[0].x )* width)
            y2 = int((hand_landmarks.landmark[0].y )* height)
            #print(zmem)
    cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 2)
    angle_calculator(x1,y1,zmem)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
######################################################################################################


################################ CLEANING UP #########################################################
arduino.close()
hands.close()