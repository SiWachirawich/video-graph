import cv2
import numpy as np

video_capture = cv2.VideoCapture('pig_vid.mp4')
frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
video_duration = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
img = cv2.imread('raw_spec.png')
h, w, _ = img.shape
img = cv2.resize(img, (w, h*2))
h, w, _ = img.shape
windows_idx = 0
windows_update = (2 if frame_rate%3 else 3)
windows_step = round((w*windows_update)/video_duration)
img = np.concatenate((np.ones((h, 640, 3), dtype=np.uint8)*255, img),axis=1)
img = np.concatenate((img, np.ones((h, 1280, 3), dtype=np.uint8)*255),axis=1)
img = np.concatenate((img, np.ones((360-h, img.shape[1], 3), dtype=np.uint8)*255),axis=0)
frame_count = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video_graph.avi', fourcc, frame_rate, (1280, 1080))

while True:
    ret, frame = video_capture.read()
    if ret != True:
        break
    frame_count += 1
    frame = cv2.resize(frame, (1280, 720))
    buffer = []

    if windows_idx+1280 < img.shape[1]:
        buffer = img[:, windows_idx:windows_idx+1280, :]
    
    frame = np.concatenate((frame, buffer),axis=0)
    if frame_count % windows_update == 0:
        windows_idx += windows_step
     
    cv2.line(frame, (640, 720), (640, 720+h), (0, 0, 255), 1)
    out.write(frame.astype(np.uint8)) 
    cv2.imshow('', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out.release()
