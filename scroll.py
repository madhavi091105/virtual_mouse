import cv2
import HandTrackingModule as htm
import pyautogui


# ==============================
# CAMERA + DETECTOR
# ==============================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)


# ==============================
# VARIABLES
# ==============================

previousY = None

scrollThreshold = 15


while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    # Mirror image
    img = cv2.flip(img, 1)


    # ==============================
    # HAND DETECTION
    # ==============================

    img = detector.findHands(img)

    lmList = detector.findPosition(img)


    if lmList:

        fingers = detector.fingersUp(lmList)


        # ==============================
        # SCROLL GESTURE
        # 🖐️ ALL FINGERS UP
        # ==============================

        if fingers == [1, 1, 1, 1, 1]:

            currentY = lmList[9][2]

            # First frame
            if previousY is None:

                previousY = currentY


            else:

                movement = previousY - currentY


                # ==============================
                # SCROLL UP
                # ==============================

                if movement > scrollThreshold:

                    pyautogui.scroll(2)

                    cv2.putText(
                        img,
                        "SCROLL UP",
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 255, 0),
                        3
                    )

                    print("SCROLL UP")


                # ==============================
                # SCROLL DOWN
                # ==============================

                elif movement < -scrollThreshold:

                    pyautogui.scroll(-2)

                    cv2.putText(
                        img,
                        "SCROLL DOWN",
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        3
                    )

                    print("SCROLL DOWN")


                # Update position
                previousY = currentY


        else:

            previousY = None


    else:

        previousY = None


    # ==============================
    # DISPLAY
    # ==============================

    cv2.imshow(
        "Scroll",
        img
    )


    # ==============================
    # QUIT
    # ==============================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================q==
# CLEANUP
# ==============================

cap.release()
cv2.destroyAllWindows()

detector.close()