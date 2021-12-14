import cv2
import numpy as np

# 변속 : 0~5
# 조향 : 0~12

# return : [변속, 조향]

"""
detect size :
    WIDTH = 60
    HEIGHT = 60

detection
    (12 tries)
    B - G - R comparison
    if R - B < weights and R - G < weights:
        True

angles
    5 * 12
"""

def getLane(frame):
    #cv2.imshow('img2', frame)
    HEIGHT, WIDTH = frame.shape[:2]
    cutWeights = 60
    # print('HEIGHT :', HEIGHT, 'WIDTH :', WIDTH)
    l_frame = frame[:,:cutWeights]
    r_frame = frame[:,WIDTH - cutWeights:]

    leftData = GetLine(l_frame, 0)
    rightData = GetLine(r_frame, 1)
    # print('left :', leftData, 'right :', rightData)
    result = leftData if leftData else rightData

    if leftData and rightData:
        result = (0, '6')

    if (not leftData and not rightData):
        result = (1,'6')
    # print('result :', result)
    return result

def GetLine(frame, position):
    text = 'left' if position == 0 else 'right'
    print("*" * 10, text, "*" * 10)
    WIDTH = frame.shape[1]
    weights = 0
    # steering_level = 6
    steering_level = 6
    BGRsss = []
    avgs = []
    max_min = []
    for i in range(12):
        ##### need HEIGHT check - (angle check) #####
        if position == 0:
            BGR = cv2.mean(frame[5 * i : 5 * (i + 1), 5 * i : 5 * (i + 1)])[:3]
        else:
            BGR = cv2.mean(frame[60 - 5 * (i + 1) : 60 - 5 * i, 5 * i : 5 * (i + 1)])[:3]
        BGRs = int((BGR[0] + BGR[1] + BGR[2]) / 3)
        BGRsss.append(BGRs)
        # if BGRs < 90:
        #     continue
        # elif BGRs < 130:
        #     weights = -2

        avgs.append((int(BGR[2] - BGR[1]), int(BGR[2] - BGR[0])))
        max_min.append([int(BGR[0]), int(BGR[1]), int(BGR[2])])
        if BGRs < 135:
            continue
        if BGRs - BGR[2] < -10:# or max(BGR) - min(BGR) > 10:
            continue

        if (BGR[2] - BGR[1] < weights and BGR[2] - BGR[0] < weights)\
                                or BGRs > 210:
            if position == 0:
                steering_level = 6 + int(i / 2)
            else:
                steering_level = int(i / 2)
                break
    print('avgs', BGRsss)
    print('Area :', avgs)
    print('Max_Min :', max_min)
    print("*" * 10)
            # else:
            #     steering_level = 12 - int(i / 2)
        # else:
        #     break
    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            print(frame[y][x])
    cv2.namedWindow('img3') if position == 0 else cv2.namedWindow('img4')
    cv2.setMouseCallback("img3", mouse_event, frame) if position == 0 else cv2.setMouseCallback("img4", mouse_event, frame)

    cv2.putText(frame, str(steering_level), (int(WIDTH / 2) - 5, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img3', frame) if position == 0 else cv2.imshow('img4', frame)
    # text = 'left - ' if position == 0 else 'right - ' 
    # text += str(steering_level)
    # print(text)
    steering_level = int(steering_level)
    print('steering_level :', steering_level)
    return False if steering_level == 6 else (1, str(steering_level))
