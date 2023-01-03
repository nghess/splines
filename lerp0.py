import cv2
import numpy as np
import random

height = 512
width = 512

canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = [int(width/2), int(height/2)]

# Points for Handles
p0 = np.array([0, -150]) + origin
p1 = np.array([-224, 200]) + origin
p2 = np.array([192, 0]) + origin
p3 = np.array([232, 192]) + origin

# Lerp for handles
def lerp(start, end, dt):
    lerp_list = []
    t = 1
    while t >= 0:
        x = int(start[0] + (end[0] - start[0]) * t)
        y = int(start[1] + (end[1] - start[1]) * t)
        lerp_list.append([x, y])
        t = round(t-dt, 2)
    return lerp_list

# Lerp for spline
def lerp_cont(l1: list, l2: list):
    lerp_list = []
    fraction = []
    for pt in range(len(l1)):
        t = pt/(len(l1)-1)
        x = int(l1[pt][0] + (l2[pt][0] - l1[pt][0]) * t)
        y = int(l1[pt][1] + (l2[pt][1] - l1[pt][1]) * t)
        lerp_list.append([x, y])
        fraction.append(round(t, 2))
    return lerp_list, fraction

# LERP Functions
dt = .02
lp0 = lerp(p0, p1, dt)
lp1 = lerp(p3, p2, dt)
spline, fraction = lerp_cont(lp0, lp1)


# Draw Spline
for i in range(len(lp0)):
    canvas = cv2.line(canvas, lp0[i], lp1[i], (32, 32, 0), 1, lineType=cv2.LINE_AA)
for i in range(len(lp0)):
    canvas = cv2.circle(canvas, spline[i], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)

# Draw Handles
canvas = cv2.circle(canvas, lp0[0], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)
canvas = cv2.circle(canvas, lp1[0], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)
canvas = cv2.circle(canvas, lp0[-1], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)
canvas = cv2.circle(canvas, lp1[-1], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)
canvas = cv2.line(canvas, p0, p1, (255, 255, 255), 1, lineType=cv2.LINE_AA)
canvas = cv2.line(canvas, p2, p3, (255, 255, 255), 1, lineType=cv2.LINE_AA)
#cv2.imwrite(f"{i}.png", canvas)
cv2.imshow('Spline', canvas)
cv2.waitKey(32)


cv2.imshow('Spline', canvas)
cv2.waitKey(100000)