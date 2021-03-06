import cv2
import mediapipe as mp
import math
import numpy as np
import requests

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#url = 'http://192.168.0.12/capture'

cap = cv2.VideoCapture(0)


def circles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, .9, 1000, param1 = 100, param2 = 40, minRadius = 0, maxRadius = 80)
    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            z = (((r-39)/8)*-5)+25
            print("Raidus = ",r,' and Distance From The Camera =  ',z)
  
            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)
  
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
            print(a," ",b)



with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
  while True:
#    img_resp = requests.get(url)
#   img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
#    image = cv2.imdecode(img_arr, -1) 
    ret, image = cap.read()  #option for webcam

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape

    circles(image)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        #print('hand_landmarks:', hand_landmarks)
        x = (hand_landmarks.landmark[4].x ) - (hand_landmarks.landmark[8].x )
        y = (hand_landmarks.landmark[4].y ) - (hand_landmarks.landmark[8].y )
        #myradians = math.degrees(math.atan2(y,x))
        #print(
        #  f'Index finger tip coordinates: (',
        #  f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        #  f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height},')
          #f'{myradians})')
          
    cv2.imshow('Z VALUE', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()