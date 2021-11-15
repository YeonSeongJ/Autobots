import cv2
import numpy as np
import LineManage as lm
import toArd

# ready to communicate with Arduino and Jetson
connect = toArd.toArduino()

# ready to get images
video_path = 0
video = cv2.VideoCapture(video_path)
HEIGHT = 0
WIDTH = 0

# ready to get average steering and speed control
speed_list = []
steering_list = []

count = 0
while video.isOpened():
    ret, frame = video.read()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)

    if not ret:
        break
    
    # get average steering and speed
    data = lm.GetLine(frame, HEIGHT, WIDTH)
    speed_list.append(data[0])
    steering_list.append(data[1])
    if count != 0 and count % 60 == 0:
        np_speed = np.array(speed_list)
        np_steering = np.array(steering_list)

        unique, counts = np.unique(np_speed, return_counts=True)
        speed = dict(zip(counts, unique))
        speed = speed[max(speed)]

        unique, counts = np.unique(np_steering, return_counts=True)
        steering = dict(zip(counts, unique))
        steering = steering[max(steering)]

        # test steering
        sends = str(steering)
        print(sends)
        connect.send(2, sends)

        speed_list = []
        steering_list = []

    count += 1

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()