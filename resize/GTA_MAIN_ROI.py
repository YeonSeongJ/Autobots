import cv2
import numpy as np
import LaneManage as lm
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
 
# valuable for stop
STOPPED = False
 
# control angle
ANGLE = 6
 
# speed control
NOW_SPEED = 1
 
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
mypath = 'images/jtest'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
 
# onlyfiles.remove('.DS_Store')
 
index = 0
for i in range(len(onlyfiles)):
    onlyfiles[i] = int(onlyfiles[i][:-4])
 
sorteds = sorted(onlyfiles)
 
for i in range(len(onlyfiles)):
    sorteds[i] = str(sorteds[i]) + '.jpg'
 
images = np.empty(len(sorteds), dtype=object)
for n in range(0, len(sorteds)):
    images[n] = cv2.imread(join(mypath, sorteds[n]))
########################################################################
# for test by images end ###############################################
########################################################################
 
cv2.namedWindow('img')
count = 0
#while video.isOpened():
 
########################################################################
# for test by images  ##################################################
########################################################################
iCount = 0
#for frame in images: 
print(len(images))
while 1:
    print('count : ', count, 'iCount :', iCount)
    frame = images[iCount]
    iCount = 0 if iCount == len(images) - 1 else iCount + 1
    s_time = time.time()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        HEIGHT = int(HEIGHT / 3)
        WIDTH = int(WIDTH / 3)
        print('width :', WIDTH, 'height :', HEIGHT)
    
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    line_check_height = int(HEIGHT / 13 * ANGLE)
    frame_cut = frame[line_check_height - 20:line_check_height + 20, int(WIDTH / 8 * 2): WIDTH - int(WIDTH / 8 * 2)]

    if not STOPPED:
        # get average steering and speed
        data = lm.getLane(frame_cut)
        speed_list.append(data[0])
        steering_list.append(data[1])
 
        # if count % 5 == 0:
        #     cv2.putText(frame, data, (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
        #     cv2.imwrite('testimages/' + str(count) + '.jpg', frame)
 
        # average fps : 35fps
        if count >= 0:
            speed = get_averages(speed_list)
            steering = get_averages(steering_list)
 
            # test steering
            sends = str(steering)
            connect.send(2, sends) if sends != '6' else print('straight')
 
            # test speed
            sends = str(speed)
            connect.send(1, str(1)) if str(NOW_SPEED) != sends else print('on speed')
            NOW_SPEED = 1
 
            speed_list = []
            steering_list = []
 
            text = 'steering : ' + str(steering) + '\nspeed : ' + str(speed)
 
        count += 1
 
    fps = int(1 / (time.time() - s_time))
 
    angText = 'angle : ' + str(ANGLE)
    cv2.putText(frame, str(fps), (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, text, (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, angText, (100,250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img', frame)
 
    input_key = cv2.waitKey(0) & 0xFF
    if  input_key == ord('q') or input_key == ord('Q'):
        break
    elif input_key == ord(',') or input_key == ord('<'):
        connect.send(2, str(4))
    elif input_key == ord('.') or input_key == ord('>'):
        connect.send(2, str(8))
    elif input_key == ord('p') or input_key == ord('P'):
        connect.send(1, str(0))
        NOW_SPEED = 0
        STOPPED = True if not STOPPED else False
    elif input_key == ord('u') or input_key == ord('U'):
        ANGLE += 1
    elif input_key == ord('d') or input_key == ord('D'):
        ANGLE -= 1
 
cv2.destroyAllWindows()
exit()