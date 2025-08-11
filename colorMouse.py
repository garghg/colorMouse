import cv2
import time
import imutils
import pyautogui

pyautogui.FAILSAFE = False

# HSV color bounds
redLower = (0, 50, 50)
redUpper = (10, 255, 255)

greenLower = (30, 100, 150)
greenUpper = (90, 255, 255)

blueLower = (80, 100, 150)
blueUpper = (130, 255, 255)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Webcam init
vs = cv2.VideoCapture(0)
time.sleep(2.0)

# Timing for click cooldowns
last_left_click = 0
last_right_click = 0
click_cooldown = 1  # seconds

while True:
    ret, frame = vs.read()
    if not ret or frame is None:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width = frame.shape[:2]

    # Resize and preprocess
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Masks
    mask_red = cv2.inRange(hsv, redLower, redUpper)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)

    mask_green = cv2.inRange(hsv, greenLower, greenUpper)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)

    # Contours
    cnts_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_red = imutils.grab_contours(cnts_red)

    cnts_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_green = imutils.grab_contours(cnts_green)

    cnts_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_blue = imutils.grab_contours(cnts_blue)

    # Track red — mouse movement
    if len(cnts_red) > 0:
        c = max(cnts_red, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            index_x = screen_width / frame_width * center[0]
            index_y = screen_height / frame_height * center[1]
            pyautogui.moveTo(index_x, index_y)

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                cv2.putText(frame, "Red - Mouse", (int(x), int(y) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Blue — Left Click
    if len(cnts_blue) > 0:
        c = max(cnts_blue, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
            cv2.putText(frame, "Blue - Left Click", (int(x), int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            if time.time() - last_left_click > click_cooldown:
                pyautogui.click()
                last_left_click = time.time()

    # Green — Right Click
    if len(cnts_green) > 0:
        c = max(cnts_green, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, "Green - Right Click", (int(x), int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if time.time() - last_right_click > click_cooldown:
                pyautogui.click(button="right")
                last_right_click = time.time()

    # Display window
    cv2.imshow("Tracking", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
vs.release()
cv2.destroyAllWindows()
