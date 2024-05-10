import cv2  # pip install opencv-contrib-python
import mediapipe as mp  # pip install mediapipe
import pyautogui    # pip install PyautoGUI


#point only index finger for cursor
#pinch using index and thumb for click
#point index and middle finger for right click
#point index,middle,ring fingers for double click

cap = cv2.VideoCapture(0)   # capture video '0' one cam
hand_detector = mp.solutions.hands.Hands()  # detect hand

drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

'''Smoothen the movement of mouse to stop at the exact position of,
   our hand movement without any shake in the movement of the mouse'''
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

while True:
    _, frame = cap.read()   # read data from cap
    '''Flip the frame or screen since the camera shows the mirror image,
       of our hand and moves in opposite direction so we need to flip the screen'''
    frame = cv2.flip(frame, 1)
     # shape gives frame height and width using shape
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # detect on rgb frame color
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks # hand landmark

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)   # see landmarks on frame
            # we use our index finger tip move the mouse
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):   # add counter
                # show the landmarks on kernel in x and y axis
                # x and y axis is multiplies by the height and width to get the x and y axis on the frames
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                # print(x,y)
                # Index finger tip point number is 8
                # and draw a boundary to the point a circle

            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):   # add counter
                # show the landmarks on kernel in x and y axis
                # x and y axis is multiplies by the height and width to get the x and y axis on the frames
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                # print(x,y)
                # Index finger tip point number is 8
                # and draw a boundary to the point a circle
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                    # pyautogui.moveTo(x,y)
                    index_x = (screen_width/frame_width)*x
                    index_y = (screen_height/frame_height)*y
                    # co-ordinates need to be changed
                    # smoothining varies with the change in the smoothening factor
                    clocx = plocx + (index_x - plocx) /smoothening
                    clocy = plocy + (index_y - plocy) /smoothening
                    pyautogui.moveTo(clocx, clocy)
                    plocx, plocy = clocx, clocy

                # thumb tip point number is 4

                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                    thumb_x = (screen_width/frame_width)*x
                    thumb_y = (screen_height/frame_height)*y
                    print('index_thumb_distance : ', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 60: #70
                        print('click')
                        pyautogui.click()
                        pyautogui.sleep(1)

                if id == 12:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                    middle_x = (screen_width/frame_width)*x
                    middle_y = (screen_height/frame_height)*y
                    print('index_middle_distance : ', abs(index_y - middle_y))
                    if abs(index_y - middle_y) < 50 and id!=16 : #70
                        print('right click')
                        pyautogui.click(button='right')
                        pyautogui.sleep(1)

                if id == 16:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(0, 255, 255))
                    ring_x = (screen_width/frame_width)*x
                    ring_y = (screen_height/frame_height)*y
                    print('index_ring_distance : ', abs(index_y - ring_y))
                    if abs(index_y - ring_y) < 50 : #70
                        print('double click')
                        pyautogui.doubleClick()
                        pyautogui.sleep(1)



    cv2.imshow('Virtual Mouse', frame)  # show image
    key=cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()# waits for key infinitely
