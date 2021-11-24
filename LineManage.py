import cv2
import numpy as np

# 변속 : 0~5
# 조향 : 0~12

# return : [변속, 조향]
def GetLine(frame, angle):
    HEIGHT, WIDTH = frame.shape[:2]
    line_check_height = int(HEIGHT / 13 * angle)
    center_point = (int(WIDTH / 2), 30)
 
    center_speed = (int(WIDTH / 2), 300)
 
    check_contour = [0,0]
 
    frame_center = (int(WIDTH / 2), line_check_height)
    m_cut = frame[line_check_height - 75:line_check_height + 75]
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)
    # 평균
    L, A, B = cv2.split(m_hsv)
    
    A = np.where(L < 190, A + 10, A)
    B = np.where(L < 190, B + 10, B)
    # a = np.where(a < 50, 50, a)
    m_hsv = cv2.merge((L, A, B))
    m_cut = cv2.cvtColor(m_hsv, cv2.COLOR_LAB2BGR)
 
    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            print(m_hsv[y][x])
 
    cv2.setMouseCallback("img", mouse_event, m_hsv)
    # HSV: (102, 28, 145)# Lab : (148, 120, 114)
    # HSV: (170, 41, 255)# Lab : (255, 142, 133)
 
    lower_color = (0, 120, 117)# HSV: (0, 40, 165)# Lab : (0, 120, 117)
    upper_color = (255, 140, 136)# HSV: (20, 60, 255)# Lab : (255, 140, 136)
    m_range = cv2.inRange(m_hsv, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)
 
    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_SIMPLE)
 
    check_contour = [0, 0]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w > 10 and h > 10 and y == 0:
            cv2.rectangle(m_result, (x, y), (x + w, y + h), (255, 0, 0), 3)
            if (x > WIDTH / 2):
                if check_contour[1] == 0:
                    check_contour[1] = x
                elif check_contour[1] > x:
                    check_contour[1] = x
                    
            else:
                if check_contour[0] == 0:
                    check_contour[0] = x + w
                elif check_contour[0] < x:
                    check_contour[0] = x + w
 
    for i in range(2):
        cv2.circle(m_result, (check_contour[i], 50), 3, (255, 0, 255), 10)
 
    got_center = int((check_contour[1] - check_contour[0]) / 2 + check_contour[0])
    cv2.circle(m_result, center_point, 3, (255, 0, 0), 10)
    cv2.circle(m_result, (got_center, 0), 3, (0, 0, 255), 5)
 
    # full screen mode
    cv2.circle(frame, frame_center, 3, (255, 0, 0), 10)
 
    # 중심제어
    text = 'on line'
    steering_level = 6
    
    if center_point[0] > got_center:
        for i in range(1, 7):
            if center_point[0] - got_center > center_point[0] / 20 * i:
                steering_level = 6 - i
                text = 'go left - level ' + str(steering_level)
 
    elif center_point[0] < got_center:
        for i in range(1, 7):
            if got_center - center_point[0] > center_point[0] / 20 * i:
                steering_level = i + 6
                text = 'go right - level ' + str(steering_level)
 
    if check_contour[0] < center_point[0] and check_contour[1] < center_point[0]:
        steering_level = 12
        text = 'go right - level ' + str(steering_level)
    elif check_contour[0] >= center_point[0] and check_contour[1] >= center_point[0]:
        steering_level = 0
        text = 'go left - level ' + str(steering_level)
    
    cv2.putText(frame, text, center_point, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
 
    cv2.imshow('img3', m_result)
    # cv2.imshow('img2', m_hsv)
 
    return (1, steering_level)