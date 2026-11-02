import cv2
import HandTrackingModule as htm
import pyautogui


# ==============================
# CAMERA + DETECTOR
# ==============================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

screenWidth, screenHeight = pyautogui.size()

rightClickDone = False


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

            rightClickDone = False

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
        # RIGHT CLICK
        # 🤟 INDEX + MIDDLE + RING
        # ==============================

        elif fingers == [0, 1, 1, 1, 0]:

            cv2.putText(
                img,
                "RIGHT CLICK",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3
            )

            # Actual right click
            if not rightClickDone:

                pyautogui.rightClick()

                rightClickDone = True

                print("RIGHT CLICK")


        # ==============================
        # OTHER GESTURE
        # ==============================

        else:

            rightClickDone = False


    # ==============================
    # DISPLAY
    # ==============================

    cv2.imshow(
        "Right Click",
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