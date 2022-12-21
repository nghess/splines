import cv2
import numpy as np
import random

height = 512
width = 512

canvas = np.zeros([512, 512])
origin = 256#[int(width/2), int(height/2)]

p0 = np.array([0, 0]) + origin
p1 = np.array([40, 96]) + origin
p2 = np.array([192, 0]) + origin
p3 = np.array([136, 144]) + origin

canvas = cv2.line(canvas, p0, p1, (255, 255, 255), 1, lineType=cv2.LINE_AA)
canvas = cv2.line(canvas, p2, p3, (255, 255, 255), 1, lineType=cv2.LINE_AA)


def lerp(point0, point1):
    lerp_points = []
    for x in range(101):
        point = p1/x
        point[point == np.inf] = 0
        point = np.array([int(point[0]), int(point[1])])
        lerp_points.append(point)
    return lerp_points

line3 = lerp(p0, p1)
#line3 = [[x for elem in line3 for x in elem]]

print(line3)

for i in range(len(line3)):
    canvas = cv2.circle(canvas, [int(line3[i][0]), int(line3[i][1])], 3, (255, 0, 0), -1, lineType=cv2.LINE_AA)
    cv2.imshow('Spline', canvas)
    cv2.waitKey(16)