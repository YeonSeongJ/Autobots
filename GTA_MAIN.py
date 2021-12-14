import cv2
import numpy as np
import LaneManage_2 as lm
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
HEIGHT = 0
WIDTH = 0
 
# valuable for stop
STOPPED = False
 
# control angle
ANGLE = 6

# steering control
prev_str = 6
str_bool = False

# speed control
NOW_SPEED = 1
 
# ready to get average steering and speed control
speed_list = []
steering_list = []

########################################################################
# for test by images  ##################################################
########################################################################
cv2.namedWindow('img')
mypath = 'images/last'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

try:
    onlyfiles.remove('.DS_Store')
except:
    print('no DS')

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

# get average
def get_averages(data_list, mode = False):
    np_list = np.array(data_list)
    unique, counts = np.unique(np_list, return_counts=True)
    result = dict(zip(counts, unique))

    direction_count = 0
    # get direction
    # left : [-x], right : [+x]
    for i in result:
        if mode == True and result[i] == '0':
            return 0

        if int(result[i]) < 6:
            direction_count -= 1
        elif int(result[i]) > 6:
            direction_count += 1

    direction = 0
    if direction_count < 0:
        direction = -1
    elif direction_count > 0:
        direction = 1

    # set degree
    onDirection = []
    for i in result:
        if direction == 0:
            break
        if result[i] == '6':
            continue

        if int(result[i]) > 6 * direction:
            onDirection.append(int(result[i]))

    #for debug
    print(result)
    if direction == 0:
        result = result[max(result)]
    else:
        result = min(onDirection) if direction == -1 else max(onDirection)
    print('result :', result)
    print("*" * 10, 'out average', "*" * 10)
    return result
 
text = ''
 
########################################################################
# for test by images  ##################################################
########################################################################
cv2.namedWindow('img')
count = 0

########################################################################
# for test by images  ##################################################
########################################################################

########################################################################
# for test by images  ##################################################
########################################################################
"""
while video.isOpened():
    s_time = time.time()
    ret, frame = video.read()

    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)
"""
for frame in images: 
    print(count * 5)
    s_time = time.time()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)

    line_check_height = int(HEIGHT / 13 * ANGLE)
    frame_cut = frame[line_check_height - 30:line_check_height + 30, int(WIDTH / 17 * 2): WIDTH - int(WIDTH / 17 * 2)]
    # cv2.imshow('img2',frame_cut)
    if not STOPPED:
        # get average steering and speed
        data = lm.getLane(frame_cut)
        speed_list.append(data[0])
        steering_list.append(data[1])
 
        # average fps : 35fps
        if count >= 0:# and count % 3 == 0:
            speed = get_averages(speed_list, True)
            steering = get_averages(steering_list)
 
            # test steering
            sends = str(steering)
            # if prev_str in ['0', '1', '2', '10', '11', '12'] and sends in ['3', '4', '5', '7', '8', '9']:
            #     str_bool = True
            # prev_str = str(steering)

            # if str_bool:
            #     str_bool = False
            # else:    
            connect.send(2, sends) if sends != '6' else print('straight')
                
            #connect.send(2, str(data[1])) 
                                                                            
            # test speed
            sends = str(speed)
            if sends == '0':
                connect.send(1, str(0))
                NOW_SPEED = 0
                # break
            connect.send(1, str(1)) if str(NOW_SPEED) != sends else print('on speed')
            NOW_SPEED = 1
 
            speed_list = []
            steering_list = []
            text = 'steering : ' + str(steering) + '\nspeed : ' + str(speed)
 
        count += 1
 
    fps = int(1 / (time.time() - s_time))
 
    cv2.putText(frame, str(fps), (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, text, (int(WIDTH / 4),int(HEIGHT / 2 - 50)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img', frame)
 
    input_key = cv2.waitKey(0) & 0xFF
    if  input_key == ord('q') or input_key == ord('Q'):
        break
    elif input_key == ord(',') or input_key == ord('<'):
        connect.send(2, str(2))
    elif input_key == ord('.') or input_key == ord('>'):
        connect.send(2, str(10))
    elif input_key == ord('p') or input_key == ord('P'):
        connect.send(1, str(0))
        NOW_SPEED = 0
        STOPPED = True if not STOPPED else False
    
cv2.destroyAllWindows()
exit()
