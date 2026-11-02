import cv2
import pyautogui
import HandTrackingModule as htm


# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

screenWidth, screenHeight = pyautogui.size()


# ==========================================
# VARIABLES
# ==========================================

leftClickDone = False
rightClickDone = False

previousY = None

scrollThreshold = 15


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    # Mirror camera
    img = cv2.flip(img, 1)


    # ==========================================
    # HAND TRACKING
    # ==========================================

    img = detector.findHands(img)

    lmList = detector.findPosition(img)


    # ==========================================
    # GESTURE GUIDE
    # ==========================================

    cv2.rectangle(
        img,
        (10, 80),
        (340, 270),
        (40, 40, 40),
        -1
    )

    cv2.putText(
        img,
        "GESTURE GUIDE",
        (25, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "1 Finger  : MOVE",
        (25, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "2 Fingers : LEFT CLICK",
        (25, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "3 Fingers : RIGHT CLICK",
        (25, 215),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "5 Fingers : SCROLL",
        (25, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    # ==========================================
    # IF HAND DETECTED
    # ==========================================

    if lmList:

        fingers = detector.fingersUp(lmList)


        # ==========================================
        # 1. MOVE CURSOR
        # ☝️ 1 FINGER
        # [0,1,0,0,0]
        # ==========================================

        if fingers == [0, 1, 0, 0, 0]:

            x = lmList[8][1]
            y = lmList[8][2]

            h, w, _ = img.shape

            screenX = int(x * screenWidth / w)
            screenY = int(y * screenHeight / h)

            pyautogui.moveTo(screenX, screenY)

            previousY = None

            cv2.putText(
                img,
                "MOVE",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                3
            )


        # ==========================================
        # 2. LEFT CLICK
        # ✌️ 2 FINGERS
        # [0,1,1,0,0]
        # ==========================================

        elif fingers == [0, 1, 1, 0, 0]:

            if not leftClickDone:

                pyautogui.click()

                leftClickDone = True

                print("LEFT CLICK")

            cv2.putText(
                img,
                "LEFT CLICK",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )


        # ==========================================
        # 3. RIGHT CLICK
        # 🤟 3 FINGERS
        # [0,1,1,1,0]
        # ==========================================

        elif fingers == [0, 1, 1, 1, 0]:

            if not rightClickDone:

                pyautogui.rightClick()

                rightClickDone = True

                print("RIGHT CLICK")

            cv2.putText(
                img,
                "RIGHT CLICK",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 0, 255),
                3
            )


        # ==========================================
        # 4. SCROLL
        # 🖐️ 5 FINGERS
        # [1,1,1,1,1]
        # ==========================================

        elif fingers == [1, 1, 1, 1, 1]:

            currentY = lmList[9][2]

            if previousY is None:

                previousY = currentY

            else:

                movement = previousY - currentY


                # SCROLL UP
                if movement > scrollThreshold:

                    pyautogui.scroll(2)

                    print("SCROLL UP")

                    cv2.putText(
                        img,
                        "SCROLL UP",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 255, 0),
                        3
                    )


                # SCROLL DOWN
                elif movement < -scrollThreshold:

                    pyautogui.scroll(-2)

                    print("SCROLL DOWN")

                    cv2.putText(
                        img,
                        "SCROLL DOWN",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 0, 255),
                        3
                    )

                previousY = currentY


        # ==========================================
        # OTHER GESTURES
        # ==========================================

        else:

            previousY = None


        # ==========================================
        # RESET CLICK STATES
        # ==========================================

        if fingers != [0, 1, 1, 0, 0]:

            leftClickDone = False


        if fingers != [0, 1, 1, 1, 0]:

            rightClickDone = False


    # ==========================================
    # NO HAND
    # ==========================================

    else:

        previousY = None

        cv2.putText(
            img,
            "NO HAND",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )


    # ==========================================
    # DISPLAY
    # ==========================================

    cv2.imshow(
        "AI Virtual Mouse",
        img
    )


    # ==========================================
    # QUIT
    # ==========================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

detector.close()