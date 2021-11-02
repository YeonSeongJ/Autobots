import cv2
import numpy as np
import LineManage

from os import listdir
from os.path import isfile, join

# mypath = 'images/2straight'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# images = np.empty(len(onlyfiles), dtype=object)
# for n in range(0, len(onlyfiles)):
#     images[n] = cv2.imread(join(mypath, onlyfiles[n]))

# HEIGHT, WIDTH = images[0].shape[:2]
# SPEED = 100

# print(HEIGHT, WIDTH)

video = cv2.VideoCapture('SaveVideo.mp4')
SPEED = 100
# for i in images:
while video.isOpened():
    ret, frame = video.read()

    HEIGHT, WIDTH = frame.shape[:2]

    if not ret:
        break

    SPEED = LineManage.GetLine(frame, HEIGHT, WIDTH, SPEED)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

