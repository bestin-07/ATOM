import cv2
import mediapipe as mp
import requests
import numpy as np

url = 'http://192.168.0.2:8080/shot.jpg'

mp_drawing1 = mp.solutions.drawing_utils
mp_drawing2 = mp.solutions.drawing_utils
mp_hands1 = mp.solutions.hands
mp_hands2 = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)


with mp_hands1.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands1 , mp_hands2.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands2:
  while cap.isOpened():
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    image1 = cv2.imdecode(img_arr, -1)  
    success, image2 = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2 = cv2.cvtColor(cv2.flip(image2, 1), cv2.COLOR_BGR2RGB)
    image1.flags.writeable = False
    image2.flags.writeable = False
    result1 = hands1.process(image1)
    result2 = hands2.process(image2)

    #Draw the hand annotations on the image.
    image1.flags.writeable = True
    image2.flags.writeable = True
    image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
    image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)

    image1_height, image1_width, _ = image1.shape
    image2_height, image2_width, _ = image2.shape

    if result1.multi_hand_landmarks and result2.multi_hand_landmarks:
      for hand_landmarks1,hand_landmarks2 in zip(result1.multi_hand_landmarks, result2.multi_hand_landmarks):
        mp_drawing1.draw_landmarks(image1, hand_landmarks1, mp_hands1.HAND_CONNECTIONS)
        mp_drawing2.draw_landmarks(image2, hand_landmarks2, mp_hands2.HAND_CONNECTIONS)

      #ALTERNATIVE OPTION

      #for hand_landmarks1 in result1.multi_hand_landmarks:
      # mp_drawing1.draw_landmarks(image1, hand_landmarks1, mp_hands1.HAND_CONNECTIONS)
      #for hand_landmarks2 in result2.multi_hand_landmarks:
      # mp_drawing2.draw_landmarks(image2, hand_landmarks2, mp_hands2.HAND_CONNECTIONS)


    cv2.imshow('MediaPipe Hands1', image1)
    cv2.imshow('MediaPipe Hands2', image2)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release() 


