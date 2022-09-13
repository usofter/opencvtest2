import subprocess
import shlex
import time
from threading import Thread
import subprocess as sp
import cv2

# rtsp_url = 'rtsp://localhost:31415/live.stream'
rtsp_url = 'rtsp://192.168.1.100:31415/live.stream'
rtsp_url2 = 'rtsp://192.168.1.102:31415/live.stream'

# video_path = 'input.mp4'
video_path = '0'

# # We have to start the server up first, before the sending client (when using TCP). See: https://trac.ffmpeg.org/wiki/StreamingGuide#Pointtopointstreaming
# ffplay_process = sp.Popen(
#     ['ffplay', '-rtsp_flags', 'listen', rtsp_url])  # Use FFplay sub-process for receiving the RTSP video.

# cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Get video frames width
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Get video frames height
# fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get video framerate
width = 640
height = 480
fps = 30

# FFmpeg command
command = ['ffmpeg',
           '-re',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-preset', 'ultrafast',
           '-f', 'rtsp',
           # '-flags', 'local_headers',
           '-rtsp_transport', 'tcp',
           '-muxdelay', '0.1',
           '-bsf:v', 'dump_extra',
           rtsp_url]

# FFmpeg command
command2 = ['ffmpeg',
           '-re',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-preset', 'ultrafast',
           '-f', 'rtsp',
           # '-flags', 'local_headers',
           '-rtsp_transport', 'tcp',
           '-muxdelay', '0.1',
           '-bsf:v', 'dump_extra',
           rtsp_url2]

p = sp.Popen(command, stdin=sp.PIPE)
p2 = sp.Popen(command2, stdin=sp.PIPE)

while (cap.isOpened()):
    ret, frame = cap.read()

    if not ret:
        break
    # time.sleep(0.2)
    p.stdin.write(frame.tobytes())
    frame2=frame.copy()
    # p2.stdin.write(frame2.tobytes())


p.stdin.close()  # Close stdin pipe
p2.stdin.close()  # Close stdin pipe
p.wait()  # Wait for FFmpeg sub-process to finish
# ffplay_process.kill()  # Forcefully close FFplay sub-process