import cv2
import HandTrackingModule as htm


# ==============================
# CAMERA + DETECTOR
# ==============================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)


while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    # Mirror image
    img = cv2.flip(img, 1)

    # Hand detection
    img = detector.findHands(img)

    # Get landmarks
    lmList = detector.findPosition(img)


    if lmList:

        # Get finger status
        fingers = detector.fingersUp(lmList)


        # =================================
        # GESTURE RECOGNITION
        # =================================

        if fingers == [0, 1, 0, 0, 0]:

            gesture = "MOVE"


        elif fingers == [0, 1, 1, 0, 0]:

            gesture = "LEFT CLICK"


        elif fingers == [0, 1, 1, 1, 0]:

            gesture = "RIGHT CLICK"


        elif fingers == [0, 1, 1, 1, 1]:

            gesture = "DRAG"


        elif fingers == [1, 1, 1, 1, 1]:

            gesture = "SCROLL"


        elif fingers == [0, 0, 0, 0, 0]:

            gesture = "NONE"


        else:

            gesture = "UNKNOWN"


        # =================================
        # DISPLAY GESTURE
        # =================================

        cv2.putText(
            img,
            gesture,
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

        # Print in terminal
        print(gesture)


    else:

        cv2.putText(
            img,
            "NO HAND",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            3
        )


    # Display
    cv2.imshow(
        "Gesture Recognition",
        img
    )


    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()

detector.close()