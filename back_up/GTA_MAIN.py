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

# get average
def get_averages(data_list):
    np_list = np.array(data_list)
    unique, counts = np.unique(np_list, return_counts=True)
    result = dict(zip(counts, unique))

    #for debug
    print(result)
    result = result[max(result)]

    return result

cv2.namedWindow('img')
count = 0
while video.isOpened():
    ret, frame = video.read()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)

    if not ret:
        break
    
    # get average steering and speed
    data = lm.GetLine(frame)
    speed_list.append(data[0])
    steering_list.append(data[1])
    if count != 0 and count % 60 == 0:
        speed = get_averages(speed_list)
        steering = get_averages(steering_list)

        # test steering
        sends = str(steering)
        connect.send(2, sends)

        # test speed
        sends = str(speed)
        connect.send(1, sends)

        speed_list = []
        steering_list = []

    count += 1

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
exit()
