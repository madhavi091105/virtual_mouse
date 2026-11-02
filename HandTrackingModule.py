import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:

    def __init__(
        self,
        model_path="hand_landmarker.task",
        maxHands=2,
        detectionCon=0.5,
        trackingCon=0.5
    ):

        self.maxHands = maxHands

        # MediaPipe model
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=maxHands,
            min_hand_detection_confidence=detectionCon,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=trackingCon
        )

        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.timestamp = 0

        # Hand connections
        self.connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]


    def findHands(self, img, draw=True):

        # BGR → RGB
        imgRGB = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        # MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=imgRGB
        )

        # Increase timestamp
        self.timestamp += 1

        # Detect
        self.results = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        # Draw landmarks
        if draw and self.results.hand_landmarks:

            h, w, _ = img.shape

            for hand in self.results.hand_landmarks:

                # Points
                for landmark in hand:

                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)

                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Connections
                for start, end in self.connections:

                    x1 = int(hand[start].x * w)
                    y1 = int(hand[start].y * h)

                    x2 = int(hand[end].x * w)
                    y2 = int(hand[end].y * h)

                    cv2.line(
                        img,
                        (x1, y1),
                        (x2, y2),
                        (255, 0, 0),
                        2
                    )

        return img


    def findPosition(self, img, handNo=0):

        lmList = []

        if not hasattr(self, "results"):
            return lmList

        if self.results.hand_landmarks:

            if handNo < len(self.results.hand_landmarks):

                hand = self.results.hand_landmarks[handNo]

                h, w, _ = img.shape

                for id, landmark in enumerate(hand):

                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)

                    lmList.append([
                        id,
                        cx,
                        cy
                    ])

        return lmList

    def fingersUp(self, lmList):
        fingers = []

        # Thumb
        if lmList[4][1] > lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Index, Middle, Ring, Pinky
        tips = [8, 12, 16, 20]

        for tip in tips:
            if lmList[tip][2] < lmList[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers



    def close(self):

        self.detector.close()