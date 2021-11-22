import cv2
import numpy as np
import LineManage as lm
import toArd
import time

# test by images
from os import listdir 
from os.path import isfile, join

# ready to communicate with Arduino and Jetson
connect = toArd.toArduino()
# check connect
connect.send(2,'0')

# ready to get images
# video_path = -1
# video = cv2.VideoCapture(video_path)
# HEIGHT = 0
# WIDTH = 0

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

text = ''

########################################################################
# for test by images  ##################################################
########################################################################
cv2.namedWindow('img')
mypath = 'images/1111'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in range(len(onlyfiles)):
    onlyfiles[i] = int(onlyfiles[i][:-4])

sorted = sorted(onlyfiles)

for i in range(len(onlyfiles)):
    sorted[i] = str(sorted[i]) + '.jpg'

images = np.empty(len(sorted), dtype=object)
for n in range(0, len(sorted)):
    images[n] = cv2.imread(join(mypath, sorted[n]))
########################################################################
# for test by images end ###############################################
########################################################################

cv2.namedWindow('img')
count = 0
#while video.isOpened():

########################################################################
# for test by images  ##################################################
########################################################################
for frame in images: 
    s_time = time.time()
    # ret, frame = video.read()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)

    # if not ret:
    #     break
    
    # get average steering and speed
    data = lm.GetLine(frame)
    speed_list.append(data[0])
    steering_list.append(data[1])

    # if count % 5 == 0:
    #     cv2.putText(frame, data, (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    #     cv2.imwrite('testimages/' + str(count) + '.jpg', frame)
    #if count != 0 and count % 30 == 0:
    if count > 0:    
        speed = get_averages(speed_list)
        steering = get_averages(steering_list)

        # test steering
        sends = str(steering)
        connect.send(2, sends)

        # test speed
        sends = str(speed)
        connect.send(1, str(1))

        speed_list = []
        steering_list = []

        text = 'steering : ' + str(steering)

    fps = int(1 / (time.time() - s_time))

    cv2.putText(frame, str(fps), (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, text, (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    count += 1
    #cv2.imshow('img', frame)

    input_key = cv2.waitKey(0) & 0xFF
    if  input_key == ord('q'):
        break
    elif input_key == ord(','):
        connect.send(2, str(4))
    elif input_key == ord('.'):
        connect.send(2, str(8))
    elif input_key == ord('p'):
        connect.send(1, str(0))
        input_key = cv2.waitKey(0) & 0xFF

cv2.destroyAllWindows()
exit()
