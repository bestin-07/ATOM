import cv2
import mediapipe as mp
import math
import numpy as np
import requests

###################  initializations  ################################################################
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

url = 'http://192.168.0.2:8080/shot.jpg'
#cap = cv2.VideoCapture(0)

x=y=0
zmem = 30 #For the memory of the previous z value and 30 is an initial z value
######################################################################################################


######################### For calculating the z value from reference sphere ##########################
def zvalue(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 200, param2 = 50, minRadius = 20, maxRadius = 60)
    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            z =  r/2.3
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
	# add a if with contiton that robot spherical ball should be within range of obtained x,y,z for robot logic to work
	xcm = (x * .02171875) - 6.95   #since we take value from half of the sceen. width = 13.9 cm  = .02171875 cm per pixel
	if z is not None:
		angle = math.degrees(math.atan2(xcm,z))
	else:
		angle = math.degrees(math.atan2(xcm,30))	
	if x > 320:
		print('RIGHT',' ',angle )		
	else:
		print('LEFT',' ',angle)
######################################################################################################


############################## Hand Detection ########################################################
with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
  while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    image = cv2.imdecode(img_arr, -1)
    image = cv2.flip(image, 1) 
#    ret, image = cap.read()  #option for webcam

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        #print('hand_landmarks:', hand_landmarks)
        x = (hand_landmarks.landmark[4].x )* image_width # - (hand_landmarks.landmark[8].x )
        y = (hand_landmarks.landmark[4].y )# - (hand_landmarks.landmark[8].y )
        #myradians = math.degrees(math.atan2(y,x))
        #print(
        #  f'Index finger tip coordinates: (',
        #  f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        #  f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height},')
          #f'{myradians})')
    

    zmem = zvalue(image)
    angle_calculator(x,y,zmem)
    print(zmem)

    cv2.imshow('MediaPipe Hands', image)
    #cv2.imshow('MediaPipe Hand', image1)
    if cv2.waitKey(5) & 0xFF == 27:
      break
######################################################################################################


cap.release()