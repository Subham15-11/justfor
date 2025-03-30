import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# parameters
width, height = 1280, 720
gestureThreshold = 400  # Threshold for gesture recognition
folder_path = "Blue Modern AI Technology Presentation"

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)  # Set width
cap.set(4, height)  # Set height


def sort_images_numerically(files):
    return sorted(
        files,
        key=lambda x: int("".join(filter(str.isdigit, x))) if x[:-4].isdigit() else x,
    )


images = sort_images_numerically(os.listdir(folder_path))

# images.sort() # strings are sorted in like 9,90,91,92
# print(images)

# variable to keep track of the current image index
imageNumber = 0
heightSmall, widthSmall = int(120 * 1.5), int(
    213 * 1.5
)  # Height and width of the webcam image
buttonPress = False  # Variable to check if the button is pressed
buttonDelay = 30  # Variable to check the delay of the button press
counter = 0  # Variable to check the counter of the button press
annotation = [[]]
annotationStart = False  # Variable to check if the annotation is started
annotationNumber = 0  # Variable to check the annotation number


# Initialize HandDetector
detector = HandDetector(
    detectionCon=0.9, maxHands=1
)  # Change the detectionCon value to adjust the hand detection accuracy

while True:
    success, img = cap.read()
    if not success:
        break

    cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect

    # load the current image
    # join the folder path with the image name
    img_path = os.path.join(folder_path, images[imageNumber])
    current_image = cv2.imread(img_path)  # Read the image from the path

    if current_image is None:
        continue

    # find the hands in the image
    hands, img = detector.findHands(img)  # Find the hands in the image

    cv2.line(
        img, (0, gestureThreshold), (width, gestureThreshold), (0, 0, 255), 2
    )  # Draw a line at the gesture threshold

    if (
        hands and buttonPress is False
    ):  # If hands are detected and button is not pressed
        hand = hands[0]
        cx, cy = hand["center"]  # Get the center of the hand
        fingers = detector.fingersUp(hand)
        # print(fingers)
        lmList = hand["lmList"]  # Get the list of landmarks of the hand
        # indexFinger = lmList[8][0] ,lmList[8][1] # Get the coordinates of the index finger

        # constrain value for easier gesture recognition
        if hand["type"] == "Right":  # If the hand is right hand
            xValue = int(np.interp(lmList[8][0], [0, width // 2], [width, 0]))
        else:
            xValue = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))

        yValue = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))

        indexFinger = xValue, yValue

        if cy < gestureThreshold:  # If the hand is above the threshold

            # GESTURE -1 :(If the thumb finger is up) LEFT SWIPE
            if fingers == [1, 0, 0, 0, 0]:
                # print("left")
                if imageNumber > 0:
                    buttonPress = True  # Set the button press to true
                    imageNumber -= 1
                    annotation = [[]]
                    annotationStart = False
                    annotationNumber = 0

            # GESTURE -2 :(If the pinky finger is up) RIGHT SWIPE
            if fingers == [0, 0, 0, 0, 1]:
                # print("right")
                if imageNumber < len(images) - 1:
                    buttonPress = True
                    imageNumber += 1
                    annotation = [[]]
                    annotationStart = False
                    annotationNumber = 0

        # GESTURE -3 :(If the index finger and middle finger are up) POINTER
        if fingers == [0, 1, 1, 0, 0]:
            # print("pointer")
            cv2.circle(current_image, indexFinger, 15, (0, 255, 0), cv2.FILLED)

        # GESTURE -4 :(If the index finger is up) DRAWING
        if fingers == [0, 1, 0, 0, 0]:
            # print("drawing")
            if annotationStart is False:  # If the annotation is not started
                annotationStart = True  # Set the annotation start to true
                annotationNumber += 1  # Increment the annotation number
                annotation.append([])  # Append a new list to the annotation list
            cv2.circle(current_image, indexFinger, 15, (0, 255, 0), cv2.FILLED)
            annotation[annotationNumber].append(
                indexFinger
            )  # Append the index finger position to the annotation list

        else:
            annotationStart = False  # Set the annotation start to false

        # GESTURE -5 :(If the index finger and middle finger and ring finger are up) POP UP
        if fingers == [0, 1, 1, 1, 0]:
            if annotation:
                annotation.pop()  # Remove the last annotation if it exists
                annotationNumber -= 1  # Decrement the annotation number
                buttonPress = True  # Set the button press to true

    else:
        # If no hands are detected or button is pressed, reset the annotation start
        annotationStart = False

    # buttonpress functionality
    if buttonPress:
        counter += 1  # Increment the counter
        if counter > buttonDelay:  # If the counter is greater than the button delay
            buttonPress = False  # Set the button press to false
            counter = 0  # Reset the counter

    # annotation functionality
    for i in range(len(annotation)):
        for j in range(len(annotation[i])):
            if j != 0:
                cv2.line(
                    current_image,
                    annotation[i][j - 1],
                    annotation[i][j],
                    (0, 0, 200),
                    7,
                )

    # add webcam image to the current image
    imageSmall = cv2.resize(img, (widthSmall, heightSmall))  # Resize the webcam image
    height, width, _ = current_image.shape  # Get the shape of the current image
    current_image[0:heightSmall, width - widthSmall : width] = (
        imageSmall  # Add the webcam image to the current image
    )

    cv2.putText(
        current_image,
        f"Slide No : {imageNumber+1}/{len(images)}",
        (50, 50),
        cv2.FONT_HERSHEY_TRIPLEX,
        1.5,
        (255, 255, 255),
        2,
    )

    # Display the image
    cv2.imshow("Subham's web camera", img)
    cv2.imshow("Presentation", current_image)  # Show the current image

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release resources
cap.release()
cv2.destroyAllWindows()
