import cv2
import HandTrackingModule as htm


cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)


while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    # Mirror image
    img = cv2.flip(img, 1)

    # Detect hand
    img = detector.findHands(img)

    # Get landmarks
    lmList = detector.findPosition(img)

    if lmList:

        # Get fingers status
        fingers = detector.fingersUp(lmList)

        # Count fingers
        totalFingers = sum(fingers)

        # Print
        print("Fingers:", totalFingers)

        # Display on screen
        cv2.putText(
            img,
            f"Fingers: {totalFingers}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            3
        )

    cv2.imshow("Finger Detection", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()