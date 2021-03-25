import cv2
import mediapipe as mp
import requests
import numpy as np


url = 'http://192.168.0.2:8080/shot.jpg'

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


'''
# For webcam input:
cap = cv2.VideoCapture('http://192.168.0.2:8080/video') #'http://192.168.0.4:8080/video'
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
'''



with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)  
    image = cv2.imdecode(img_arr, -1)


    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)   
    #image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    #image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    #image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        #print('hand_landmarks:', hand_landmarks)
        print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})')
         # f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z })')
          
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()