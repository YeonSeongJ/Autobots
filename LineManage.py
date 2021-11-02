import cv2
import numpy as np
import time

def GetLine(frame, HEIGHT, WIDTH, SPEED):
    start_time = time.time()
    line_check_height = int(HEIGHT / 9 * 4)
    speed_check_height = int(HEIGHT / 9 * 2)
    center_point = (int(WIDTH / 2), 30)

    center_speed = (int(WIDTH / 2), 300)

    check_contour = [0,0]

    frame_center = (int(WIDTH / 2), line_check_height)

    m_cut = frame[line_check_height - 50:line_check_height + 50,0:WIDTH ]
    m_speed_cut = frame[speed_check_height - 50:speed_check_height + 50,0:WIDTH ]
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)

    lower_color = (190, 127, 0)#(0, 138, 134)#(226, 175, 169)
    upper_color = (237, 144, 255)#(255, 165, 152)#(255, 255, 255)

    m_range = cv2.inRange(m_hsv, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)
    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_NONE)
    check_contour = [0, 0]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if y == 0:
            # print('cnt :', x, y)
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
    speed = 'speed up'
    return_speed = SPEED
    tf = False
    if center_point[0] > got_center:
        for i in range(15):
            if center_point[0] - got_center < 30 * i:
                if i > 1:
                    text = 'go left - ' + str(i) + '%'
                    speed = 'speed down ' + str(i) + 'km/s'
                    if SPEED > 100 - i * 5:
                        return_speed -= i * 5
                        tf = True

                    # print('go left -', str(i) + '%')
                    break
    elif center_point[0] < got_center:
        for i in range(15):
            if got_center - center_point[0] < 30 * i:
                if i > 1:
                    text = 'go right - ' + str(i) + '%'
                    speed = 'speed down ' + str(i) + 'km/s'
                    if SPEED > 100 - i * 5:
                        return_speed -= i * 5
                        tf = True
                    # print('go right -',str(i) + '%')
                    break

    cv2.putText(frame, text, center_point, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    if tf != True:
        speed = 'good speed'
    cv2.putText(frame, speed, center_speed, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    fps = int(1 / (time.time() - start_time))
    # cv2.putText(frame, str(fps) + 'fps', (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, cv2.LINE_AA)
    
    cv2.imshow('img', m_result)
    cv2.imshow('img2', m_cut)
    cv2.imshow('img3', m_speed_cut)
    cv2.imshow('full screen', frame)

    return return_speed