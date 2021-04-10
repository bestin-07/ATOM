
######################### For calculating the z value from reference sphere ##########################
import cv2
import numpy as np
def zvalue(image):
    zmem = 30 #For the memory of the previous z value and 30 is an initial z value
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = 200, param2 = 50, minRadius = 20, maxRadius = 60)
    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            z =  r
            #print(r,' ',z)
            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (0, 255, 0), 2)
  
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
            return z
    else:
        return zmem
######################################################################################################