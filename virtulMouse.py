import cv2
import HandTrackingModule as htm
import pyautogui

screenWidth, screenHeight = pyautogui.size()

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

while True:

    success, img = cap.read()

    if not success:
        print("Camera se frame nahi aa raha")
        break

    img = cv2.flip(img, 1)

    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    if lmList:

        # Index finger tip
        x = lmList[8][1]
        y = lmList[8][2]

        h, w, _ = img.shape

        # Camera → Screen
        screenX = int(x * screenWidth / w)
        screenY = int(y * screenHeight / h)

        # Move cursor
        pyautogui.moveTo(screenX, screenY)

        # Mark index finger
        cv2.circle(
            img,
            (x, y),
            10,
            (0, 255, 0),
            -1
        )

    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
detector.close()