import cv2
import numpy as np
import lane as lm

# test by images
from os import listdir 
from os.path import isfile, join

# for perceptron
rate = 0.01
sum_error = 0.0
prev_error = 0.0
pos_neg = 1

# control angle
ANGLE = 6

cv2.namedWindow('img')
mypath = 'images/testimage1'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
 
onlyfiles.remove('.DS_Store')
 
index = 0
for i in range(len(onlyfiles)):
    onlyfiles[i] = int(onlyfiles[i][:-4])

sorteds = sorted(onlyfiles)
 
for i in range(len(onlyfiles)):
    sorteds[i] = str(sorteds[i]) + '.jpg'
 
images = np.empty(len(sorteds), dtype=object)
for n in range(0, len(sorteds)):
    images[n] = cv2.imread(join(mypath, sorteds[n]))
print('#######  read done  #######')
########################################################################
# for test by images end ###############################################
########################################################################
 
def setWeights():
    global sum_error, rate, pos_neg
    sum_error += 1

    file = open('weights.txt', 'r')
    GB_WEIGHTS = int(float(file.readline()[:-1]))
    R_WEIGHTS = int(float(file.readline()[:-1]))
    BIAS = int(float(file.readline()))
    file.close()

    file = open('weights.txt', 'w')
    text = ''
    # GB_WEIGHTS
    GB_WEIGHTS += rate * GB_WEIGHTS * pos_neg
    text += str(GB_WEIGHTS) + '\n'
    # R_WEIGHTS
    R_WEIGHTS += rate * R_WEIGHTS * pos_neg
    text += str(R_WEIGHTS) + '\n'
    # BIAS
    BIAS = BIAS + rate * pos_neg
    text += str(BIAS)
    file.write(text)
    file.close()

cv2.namedWindow('img')
count = 0
HEIGHT = 0
WIDTH = 0

breaks = False
while 1:
    for frame in images:
        if count == 0:
            HEIGHT, WIDTH = frame.shape[:2]
            # print('width :', WIDTH, 'height :', HEIGHT)
        
        line_check_height = int(HEIGHT / 13 * ANGLE)
        frame_cut = frame[line_check_height - 50:line_check_height + 50, int(WIDTH / 8 * 2): WIDTH - int(WIDTH / 8 * 2)]
    
        # get average steering and speed
        data = lm.getLane(frame_cut)

        input_key = cv2.waitKey(0) & 0xFF
        if  input_key == ord('q') or input_key == ord('Q'):
            breaks = True
            break
        elif input_key == ord('1'):
            pass
        elif input_key == ord('2'):
            setWeights()

        count += 1
        if count % 7 == 0:
            print('prev : %.3f' % prev_error, '\nnow : %.3f' % (sum_error / 7))
            pos_neg *= -1 if prev_error > sum_error / 7 else 1
            prev_error = sum_error / 7
            print('err_rate by 7 trial : %.3f' % prev_error)
            
            sum_error = 0

    if breaks:
        break

cv2.destroyAllWindows()
exit()