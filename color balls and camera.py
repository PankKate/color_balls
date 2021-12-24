
"""
Created on Fri Dec 24 14:37:07 2021

@author: PankK
"""

import cv2
import numpy as np
import time
from random import randint

def color_diap(h):
    return {
               h < 13: 'Red',
        13 <= h < 35: 'Yellow',
        35 <= h < 80:  'Green',
        80 <= h < 145:  'Blue',
        145 <= h:       'Red'
    }[True]

def program_colors():
    colors = ['Red','Yellow','Green','Blue']
    quessed = []
    while len(quessed) != 3:
        checked = colors[randint(0, 3)]
        if checked not in quessed:
            quessed.append(checked)
    return(quessed)

if __name__ == '__main__':
    def callback(*arg):
        print (arg)

quessed = program_colors()
print(quessed)
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("Camera")


blue_min = np.array((90, 120, 90), np.uint8)
blue_max = np.array((150, 255, 255), np.uint8)
green_min = np.array((40, 120, 90), np.uint8)
green_max = np.array((80, 255, 255), np.uint8)
red_min = np.array((160, 120, 90), np.uint8)
red_max = np.array((180, 255, 255), np.uint8)
yellow_min = np.array((13, 120, 90), np.uint8)
yellow_max = np.array((35, 255, 255), np.uint8)

while True:
    flag, img = cam.read()
    # преобразуем RGB картинку в HSV модель
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
     
    thresh_1= cv2.inRange(hsv, blue_min, blue_max)
    thresh_2= cv2.inRange(hsv, green_min, green_max)
    thresh_3= cv2.inRange(hsv, red_min, red_max)
    thresh_4= cv2.inRange(hsv, yellow_min, yellow_max)
    
    thresh = thresh_1 + thresh_2 + thresh_3 + thresh_4
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    data = {}
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(img, ((x+x+w)//2, (y+y+h)//2), 4, (0,255,0), -1)
            hsv_color = hsv[(y+y+h)//2, (x+x+w)//2][0]
            color = color_diap(hsv_color)
            
            data[color] = x
            
     
            
        cv2.imshow("Background", thresh)
    cv2.imshow("Camera", img)
    if len(data)>2:
        sorted_data = {}
        sorted_keys = sorted(data, key=data.get)  
        for w in sorted_keys:
            sorted_data[w] = data[w]
     
        user_colors = list(sorted_data)
        
        if(quessed == user_colors ):
            print("Right")
            time.sleep(1)
            break
    
   
    ch = cv2.waitKey(5)
    if ch == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()