# r = 66
# g = 134
# b = 244
#
# if(r > thresh) r = 255 else r = 0; // we have r = 0
# if(g > thresh) g = 255 else g = 0; // we have g = 0
# if(b > thresh) b = 255 else b = 0; // we have b = 255

from sys import argv
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    (_, frame) = cap.read()

    # Conversion to CMYK (just the K channel):

    # Convert to float and divide by 255:
    imgFloat = frame.astype(np.float64) / 255.

    # Calculate channel K:
    kChannel = 1 - np.max(imgFloat, axis=2)

    # Convert back to uint 8:
    kChannel = (255 * kChannel).astype(np.uint8)

    # Threshold image:
    binaryThresh = 190
    _, binaryImage = cv2.threshold(kChannel, binaryThresh, 255, cv2.THRESH_BINARY)

    # ret, threshold = cv2.threshold(frame, 120, 255, cv2.THRESH_BINARY)

    cv2.imshow('threshold', binaryImage)
    # cv2.imshow('ori', img)
    cv2.waitKey(1)
