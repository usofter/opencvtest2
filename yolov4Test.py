import cv2
import imutils
import numpy as np
import random
import colorsys


# inspiration and some code pieces were copied from https://github.com/haroonshakeel/yolo_get_preds/blob/master/my_utils.py

def get_random_bright_colors(size):
    for i in range(0, size - 1):
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
        yield (r, g, b)


def get_yolo_preds(net, confidence_threshold, overlapping_threshold, video_url=None,labels=10, frame_resize_width=[224,128]):
    # List of colors to represent each class label with distinct bright color
    # colors = list(get_random_bright_colors(len(labels)))
    colors = list(get_random_bright_colors(labels))

    ln = net.getLayerNames()
    # ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    # cap = cv2.VideoCapture(video_url)
    #
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # frame = cv2.imread("bottle_number_test.jpg")
    try:
        # if not cap.isOpened():
        #     print("Error opening video stream or file")
        #     return


        yolo_width_height = (320, 224)

        counter = 0
        max_count = 0

        while True:
            (_, frame) = cap.read()
            number_text=""
            frame= cv2.resize(frame, (1920,1080), interpolation = cv2.INTER_AREA)
            # x, y, w, h = 300, 120, 140, 40
            x, y, w, h = 820, 480, 240, 120
            frame = frame[y:y + h, x:x + w]

            counter += 1

            if frame_resize_width:
                frame = imutils.resize(frame, width=frame_resize_width[0],height=frame_resize_width[1])
            (H, W) = frame.shape[:2]

            # Construct blob of frames by standardization, resizing, and swapping Red and Blue channels (RBG to RGB)
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, yolo_width_height, swapRB=True, crop=False)
            net.setInput(blob)
            layerOutputs = net.forward(ln)
            boxes = []
            confidences = []
            classIDs = []
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > confidence_threshold:
                        # Scale the bboxes back to the original image size
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            # Remove overlapping bounding boxes
            bboxes = cv2.dnn.NMSBoxes(
                boxes, confidences, confidence_threshold, overlapping_threshold)
            if len(bboxes) > 0:
                for i in bboxes.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    color = [int(c) for c in colors[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    # text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
                    # text = str(labels[classIDs[i]])+",conf  "+str(confidences[i])
                    text = str(classIDs[i])+",conf  "+str(confidences[i])
                    number_text+=str(classIDs[i])
                    # draw bounding box title background
                    text_offset_x = x
                    text_offset_y = y
                    text_color = (255, 255, 255)
                    (text_width, text_height) = \
                    cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, thickness=1)[0]
                    box_coords = (
                    (text_offset_x, text_offset_y), (text_offset_x + text_width - 80, text_offset_y - text_height + 4))
                    cv2.rectangle(frame, box_coords[0], box_coords[1], color, cv2.FILLED)

                    # draw bounding box title
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

            cv2.putText(frame, number_text, (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

            # if len(bboxes) > max_count:
            #    max_count = len(bboxes)
            #    cv2.imwrite('captured_' + str(counter) + '.jpg', frame)
            cv2.imshow("YOLOv4 Object Detection", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break the loop
            if key == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


with open("digits_v1.names", "r", encoding="utf-8") as f:
    labels = f.read().strip().split("\n")

yolo_config_path = "yolov4-tiny-custom_digits_v1_320x224.cfg"
yolo_weights_path = "yolov4-tiny-custom_digits_v1_320x224_100000.weights"
yolo_weights_path = "yolov4-tiny-custom_digits_v1_320x224_best.weights"

useCuda = True

net = cv2.dnn.readNetFromDarknet(yolo_config_path, yolo_weights_path)

if useCuda:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# video_url = "https://cdn-004.whatsupcams.com/hls/hr_pula01.m3u8"
frame_width = 600

if __name__ == '__main__':
    get_yolo_preds(net, 0.2, 0.2, labels, frame_width)