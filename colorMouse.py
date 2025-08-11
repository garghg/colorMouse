import cv2
import time
import imutils
import pyautogui
pyautogui.FAILSAFE = False

redLower = (0, 50, 50)
redUpper = (10, 255, 255)

greenLower = (30, 100, 150)
greenUpper = (90, 255, 255)

blueLower = (80, 100, 150)
blueUpper = (130, 255, 255)

screen_width, screen_height = pyautogui.size()

vs = cv2.VideoCapture(0)

time.sleep(2.0)


while True:
    _, frame = vs.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #find the red on the video and isolate just the red parts
    mask_red = cv2.inRange(hsv, redLower, redUpper)
    #remove the small excess pathes on red pixels dtected like a reddish shade on hand etc. iterates 2 times
    mask_red = cv2.erode(mask_red, None, iterations=2)
    #fills in the removed pixels from erode with neighbouring pixels
    mask_red = cv2.dilate(mask_red, None, iterations=2)

    #green
    mask_green = cv2.inRange(hsv, greenLower, greenUpper)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)
    green_detected = cv2.countNonZero(mask_green) > 0

    #blue
    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)
    blue_detected = cv2.countNonZero(mask_blue) > 0

    cnts_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #convert sthe contours into a friendlier list
    cnts_red = imutils.grab_contours(cnts_red)

    cnts_green = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_green = imutils.grab_contours(cnts_green)

    cnts_blue = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_blue = imutils.grab_contours(cnts_blue)

    center = None

    if len(cnts_red) > 0:
        #finds the largest contour and tracks it 
        c = max(cnts_red, key=cv2.contourArea)
        #calculates how big the circle around the contour should be
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #find the center of the contour to place the circle
        M = cv2.moments(c)
        #stored the centroid as integers
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
        index_x = screen_width/frame_width*center[0]
        index_y = screen_height/frame_height*center[1]
        pyautogui.moveTo(index_x, index_y)

        if radius > 10:
            #the circle around the tracked object
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)