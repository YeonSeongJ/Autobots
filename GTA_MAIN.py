import cv2
import numpy as np
import LineManage as lm
import toArd
import time
 
# ready to communicate with Arduino and Jetson
connect = toArd.toArduino()
# check connect
connect.send(2,'0')

# ready to get images
video_path = -1
video = cv2.VideoCapture(video_path)
HEIGHT = 0
WIDTH = 0
 
# ready to get average steering and speed control
speed_list = []
steering_list = []
 
# valuable for stop
STOPPED = False
 
# angle controller
ANGLE = 5
 
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
 
cv2.namedWindow('img')
count = 0
while video.isOpened():
    s_time = time.time()
    ret, frame = video.read()
    if count == 0:
        HEIGHT, WIDTH = frame.shape[:2]
        print('width :', WIDTH, 'height :', HEIGHT)
 
    if not ret:
        break
    
    if not STOPPED:
        # get average steering and speed
        data = lm.GetLine(frame, ANGLE)
        speed_list.append(data[0])
        steering_list.append(data[1])
 
        if count % 5 == 0:
            cv2.putText(frame, str(data), (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.imwrite('testimages/' + str(count) + '.jpg', frame)
 
        # average fps : 35fps
        if count != 0 and count % 10 == 0:
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
 
            text = 'steering : ' + str(steering) + '||| speed : ' + str(speed)
 
        count += 1
 
    fps = int(1 / (time.time() - s_time))
 
    angText = 'angle : ' + str(ANGLE)
 
    cv2.putText(frame, str(fps), (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, text, (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, angText, (100, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img', frame)
 
    input_key = cv2.waitKey(1) & 0xFF
    if  input_key == ord('q') or input_key == ord('Q'):
        break
    elif input_key == ord(',') or input_key == ord('<'):
        connect.send(2, str(4))
    elif input_key == ord('.') or input_key == ord('>'):
        connect.send(2, str(8))
    elif input_key == ord('p') or input_key == ord('P'):
        connect.send(1, str(0))
        STOPPED = True if STOPPED == False else False
    elif input_key == ord('u') or input_key == ord('U'):
        ANGLE -= 1
    elif input_key == ord('d') or input_key == ord('D'):
        ANGLE += 1
 
cv2.destroyAllWindows()
exit()