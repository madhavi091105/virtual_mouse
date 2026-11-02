import cv2
import HandTrackingModule as htm
import pyautogui


# ==============================
# CAMERA + DETECTOR
# ==============================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

screenWidth, screenHeight = pyautogui.size()

clickDone = False


while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    img = cv2.flip(img, 1)

    # ==============================
    # HAND DETECTION
    # ==============================

    img = detector.findHands(img)

    lmList = detector.findPosition(img)


    if lmList:

        fingers = detector.fingersUp(lmList)


        # ==============================
        # CURSOR MOVEMENT
        # ☝️ INDEX ONLY
        # ==============================

        if fingers == [0, 1, 0, 0, 0]:

            x = lmList[8][1]
            y = lmList[8][2]

            h, w, _ = img.shape

            screenX = int(x * screenWidth / w)
            screenY = int(y * screenHeight / h)

            pyautogui.moveTo(
                screenX,
                screenY
            )

            clickDone = False

            cv2.putText(
                img,
                "MOVE",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                3
            )


        # ==============================
        # LEFT CLICK
        # ✌️ INDEX + MIDDLE
        # ==============================

        elif fingers == [0, 1, 1, 0, 0]:

            cv2.putText(
                img,
                "LEFT CLICK",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3
            )

            # Actual mouse click
            if not clickDone:

                pyautogui.click()

                clickDone = True

                print("LEFT CLICK")


        # ==============================
        # OTHER GESTURE
        # ==============================

        else:

            clickDone = False


    # ==============================
    # DISPLAY
    # ==============================

    cv2.imshow(
        "Left Click",
        img
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# CLEANUP
# ==============================

cap.release()
cv2.destroyAllWindows()

detector.close()