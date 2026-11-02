import cv2
import math
import HandTrackingModule as htm
import pyautogui


# ==============================
# CAMERA + DETECTOR
# ==============================

cap = cv2.VideoCapture(0)

detector = htm.HandDetector(maxHands=1)

screenWidth, screenHeight = pyautogui.size()

dragging = False


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

        # ==============================
        # INDEX + THUMB POSITION
        # ==============================

        indexX = lmList[8][1]
        indexY = lmList[8][2]

        thumbX = lmList[4][1]
        thumbY = lmList[4][2]


        # ==============================
        # CURSOR MOVEMENT
        # ==============================

        h, w, _ = img.shape

        screenX = int(indexX * screenWidth / w)
        screenY = int(indexY * screenHeight / h)


        # ==============================
        # PINCH DISTANCE
        # ==============================

        distance = math.hypot(
            indexX - thumbX,
            indexY - thumbY
        )


        # ==============================
        # DRAG START
        # ==============================

        if distance < 40:

            if not dragging:

                pyautogui.moveTo(
                    screenX,
                    screenY
                )

                pyautogui.mouseDown()

                dragging = True

                print("DRAG START")


            # ==============================
            # DRAG MOVEMENT
            # ==============================

            pyautogui.moveTo(
                screenX,
                screenY
            )

            cv2.putText(
                img,
                "DRAGGING",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3
            )


        # ==============================
        # RELEASE DRAG
        # ==============================

        else:

            if dragging:

                pyautogui.mouseUp()

                dragging = False

                print("DRAG END")


            # Normal cursor movement
            pyautogui.moveTo(
                screenX,
                screenY
            )

            cv2.putText(
                img,
                "MOVE",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                3
            )


    else:

        # Safety: release mouse if hand disappears
        if dragging:

            pyautogui.mouseUp()

            dragging = False

            print("DRAG END")


    # ==============================
    # DISPLAY
    # ==============================

    cv2.imshow(
        "Drag",
        img
    )


    # ==============================
    # QUIT
    # ==============================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# CLEANUP
# ==============================

if dragging:
    pyautogui.mouseUp()

cap.release()
cv2.destroyAllWindows()

detector.close()