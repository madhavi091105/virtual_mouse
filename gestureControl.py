import cv2
import HandTrackingModule as htm
import pyautogui
import time


cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

screenWidth, screenHeight = pyautogui.size()

# Click control
clickDone = False


while True:

    success, img = cap.read()

    if not success:
        print("Camera frame nahi aa raha")
        break

    img = cv2.flip(img, 1)

    # Hand detection
    img = detector.findHands(img)

    # Landmarks
    lmList = detector.findPosition(img)

    if lmList:

        # Get fingers
        fingers = detector.fingersUp(lmList)

        # --------------------------------
        # INDEX ONLY = MOVE CURSOR
        # --------------------------------

        if fingers == [0, 1, 0, 0, 0]:

            x = lmList[8][1]
            y = lmList[8][2]

            h, w, _ = img.shape

            screenX = int(x * screenWidth / w)
            screenY = int(y * screenHeight / h)

            pyautogui.moveTo(screenX, screenY)

            clickDone = False

            cv2.putText(
                img,
                "MOVE",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                3
            )


        # --------------------------------
        # INDEX + MIDDLE = LEFT CLICK
        # --------------------------------

        elif fingers == [0, 1, 1, 0, 0]:

            cv2.putText(
                img,
                "LEFT CLICK",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3
            )

            if not clickDone:

                print("CLICK!")

                pyautogui.click()

                clickDone = True


        # --------------------------------
        # OTHER
        # --------------------------------

        else:

            clickDone = False


    cv2.imshow(
        "Gesture Control",
        img
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()