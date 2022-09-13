import subprocess as sp
import cv2

# rtsp_url = 'rtsp://localhost:31415/live.stream'
rtsp_url = 'rtsp://192.168.1.101:31415/ch0'

# video_path = 'input.mp4'
video_path = '0'

# We have to start the server up first, before the sending client (when using TCP). See: https://trac.ffmpeg.org/wiki/StreamingGuide#Pointtopointstreaming
ffplay_process = sp.Popen(
    ['ffplay', '-rtsp_flags', 'listen', rtsp_url])  # Use FFplay sub-process for receiving the RTSP video.
c=0
while (True):
    c=c+1

ffplay_process.kill()
