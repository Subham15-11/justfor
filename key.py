# opencv,cvzone,mediapipe,numpy,pynput
import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller


# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

# Initialize HandDetector
detector = HandDetector(detectionCon=0.8)

keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
]

finalText = ""

keyboard = Controller()


# for normal buttons
"""def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(
            img,
            button.text,
            (x + 20, y + 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            4,
        )
    return img"""


# For transparency
def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(
            imgNew,
            (button.pos[0], button.pos[1], button.size[0], button.size[1]),
            20,
            rt=0,
        )
        cv2.rectangle(
            imgNew,
            button.pos,
            (x + button.size[0], y + button.size[1]),
            (0, 0, 0),
            cv2.FILLED,
        )
        cv2.putText(
            imgNew,
            button.text,
            (x + 40, y + 60),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 255, 255),
            3,
        )

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    # print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    """def draw(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(
            img,
            self.text,
            (x + 20, y + 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            4,
        )
        return img"""


buttonList = []
# putting all keys
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    # Capture frame from webcam
    success, img = cap.read()
    if not success:
        break

    # Detect hands
    hands, img = detector.findHands(img)  # Returns list of hands and the image
    if hands:
        # Get details of the first hand detected
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 landmark points (x, y, z)
        bbox = hand["bbox"]  # Bounding box (x, y, w, h)
        center = hand["center"]  # Center of the hand (cx, cy)
        handType = hand["type"]  # 'Left' or 'Right'

        # Print details
        # print(f"Hand Type: {handType}, Center: {center}, Bounding Box: {bbox}")

    # cv2.rectangle(img,(100,100),(200,200),(0,0,0),cv2.FILLED)
    # cv2.putText(img,"Q",(125,170),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

    # img = myBotton.draw(img)
    # for showing buttons
    img = drawAll(img, buttonList)

    # Display the resulting frame
    if hands:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(
                    img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED
                )
                cv2.putText(
                    img,
                    button.text,
                    (x + 20, y + 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 0),
                    5,
                )
                length, info, img = detector.findDistance(
                    lmList[8][:2], lmList[12][:2], img
                )
                # print(length)

                if length < 40:
                    cv2.rectangle(
                        img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED
                    )
                    cv2.putText(
                        img,
                        button.text,
                        (x + 20, y + 65),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (0, 255, 0),
                        5,
                    )

                    finalText += button.text
                    keyboard.press(button.text)
                    sleep(0.40)

    cv2.rectangle(img, (50, 450), (700, 600), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, finalText, (80, 550), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

    # Display the image
    cv2.imshow("Image", img)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
