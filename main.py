
import cv2
import numpy as np

def show_webcam(mirror=False,WebCamNum=0):
    # cam = cv2.VideoCapture(WebCamNum)
    cam = cv2.VideoCapture("rtsp://localhost:8554/live.stream2")
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    # fourcc=cv2.VideoWriter_fourcc(*'VIDX')
    videoWriter = cv2.VideoWriter(r'C:\Users\DS\PycharmProjects\video_ECON.avi',fourcc,30,(1920,1080))
    # videoWriter = cv2.VideoWriter(r'C:\Users\DS\PycharmProjects\video_ECON.avi', fourcc, 30.0, (640,480))

    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
            # dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
            # dft = cv2.dft(img)

        if ret_val:
            cv2.imshow('video', img)
            # videoWriter.write(img)

        # cv2.imshow('dft', dc)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()


def main():
    show_webcam()


if __name__ == '__main__':
    main()