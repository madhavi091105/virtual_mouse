import cv2
import HandTrackingModule as htm


cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)


while True:

    success, img = cap.read()

    if not success:
        print("Camera frame nahi aa raha")
        break

    img = cv2.flip(img, 1)

    # Hand detect
    img = detector.findHands(img)

    # Get landmarks
    lmList = detector.findPosition(img)

    if lmList:

        # IMPORTANT: check landmarks


        fingers = detector.fingersUp(lmList)

        print("Finger list:", fingers)

        totalFingers = sum(fingers)

        print("Total fingers:", totalFingers)

        cv2.putText(
            img,
            "Fingers: " + str(totalFingers),
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            3
        )

    else:

        cv2.putText(
            img,
            "No Hand",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            3
        )

    cv2.imshow("Finger Detection", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()