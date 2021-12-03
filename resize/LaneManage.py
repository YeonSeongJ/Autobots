import cv2
import numpy as np

# 변속 : 0~5
# 조향 : 0~12

# return : [변속, 조향]

LIGHTNESS_LEFT = (0,0,0)
LIGHTNESS_RIGHT = (0,0,0)

def getLane(frame):
    
    HEIGHT, WIDTH = frame.shape[:2]
    cv2.imshow('img2', frame)
    cutWeights = 0

    l_frame = frame[:,:HEIGHT]
    r_frame = frame[:,WIDTH - HEIGHT:]

    setLightness(l_frame, 0)
    setLightness(r_frame, 1)

    leftData = GetLine(l_frame, 0)
    rightData = GetLine(r_frame, 1)
    # print('left :', leftData, 'right :', rightData)
    result = leftData if leftData else rightData

    if (leftData and rightData) or (not leftData and not rightData):
        result = (1,'6')
    # print('result :', result)
    return result

def GetLine(frame, position):
    WIDTH = frame.shape[1]    
    check_contour = [0,0]

    lower_color = convertLightness(position)
    upper_color = (255, 255, 255)
    print('low :', lower_color, 'upper :', upper_color)
    m_range = cv2.inRange(frame, lower_color, upper_color)
    m_result = cv2.bitwise_and(frame, frame, mask=m_range)
 
    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_SIMPLE)

    # get lines
    check_contour = [0, 0]
    contours_count = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 5 and h > 5 and y == 0:
            if (position == 0 and x == 0) or (position == 1 and x + w == WIDTH):
                contours_count += 1
                cv2.rectangle(m_result, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # right
            if position == 1:
                if check_contour[0] == 0:
                    check_contour = (w, x)
                elif check_contour[1] > x:
                    check_contour = (w, x)
            # left
            else:
                if check_contour[0] == 0:
                    check_contour = (w, x + w)
                elif check_contour[1] < x:
                    check_contour = (w, x + w)

    cv2.circle(m_result, (check_contour[0], 50), 3, (255, 0, 255), 10)
    
    # 중심제어
    text = 'on line'
    steering_level = 6
    
    if position == 0:
        for i in range(1, 7):
            if check_contour[0] > 30 * i:
                steering_level += 1
                text = 'go right - ' + str(steering_level - 6)
    elif position == 1:
        for i in range(1, 7):
            if check_contour[0] > 30 * i:
                steering_level -= 1
                text = 'go left - ' + str(6 - steering_level)

    # cv2.putText(frame, text, (int(WIDTH / 2), 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img3', m_result) if position == 0 else cv2.imshow('img4', m_result)
    text = 'left - ' if position == 0 else 'right - ' 
    text += str(steering_level)
    print(text)
    return False if contours_count == 0 else (1, str(steering_level))

def convertLightness(position):
    global LIGHTNESS_LEFT, LIGHTNESS_RIGHT
    text = LIGHTNESS_LEFT if position == 0 else LIGHTNESS_RIGHT
    # print(str(position) + ' :', text)
    B = 40
    G = 40
    R = -50
    weights = 10
    if position == 0:
        B += (LIGHTNESS_LEFT[0] - weights) * (LIGHTNESS_LEFT[0] - weights) / 100
        G += (LIGHTNESS_LEFT[1] - weights) * (LIGHTNESS_LEFT[1] - weights) / 100
        R += (LIGHTNESS_LEFT[2] - weights) * (LIGHTNESS_LEFT[2] - weights) / 100
        print('LIGHTNESS_LEFT :', LIGHTNESS_LEFT)
    elif position == 1:
        B += (LIGHTNESS_RIGHT[0] - weights) * (LIGHTNESS_RIGHT[0] - weights) / 100
        G += (LIGHTNESS_RIGHT[1] - weights) * (LIGHTNESS_RIGHT[1] - weights) / 100
        R += (LIGHTNESS_RIGHT[2] - weights) * (LIGHTNESS_RIGHT[2] - weights) / 100
        print('LIGHTNESS_RIGHT :', LIGHTNESS_RIGHT)
    return B, G, R

def setLightness(frame, position):
    global LIGHTNESS_LEFT, LIGHTNESS_RIGHT
    if position == 0:
        LIGHTNESS_LEFT = cv2.mean(frame)
        print('left light :', LIGHTNESS_LEFT)
    elif position == 1:
        LIGHTNESS_RIGHT = cv2.mean(frame)
        print('right light :', LIGHTNESS_RIGHT)
    return

