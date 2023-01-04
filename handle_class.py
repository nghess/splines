import cv2
import numpy as np

# Lerp for handles
def lerp(start, end, dt):
    lerp_list = []
    t = 1
    while t >= 0:
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        lerp_list.append([x, y])
        t = round(t-dt, 2)
    return np.int32(lerp_list)

# Lerp for spline
def lerp_spline(l1, l2):
    lerp_list = []
    for pt in range(len(l1)):
        t = pt/(len(l1)-1)
        x = l1[pt][0] + (l2[pt][0] - l1[pt][0]) * t
        y = l1[pt][1] + (l2[pt][1] - l1[pt][1]) * t
        lerp_list.append([x, y])
    return np.int32(lerp_list)


class Handle:

    def __init__(self, x, y):
        self.h = False
        self.x = x + origin[0]
        self.y = y + origin[1]
        self.pt = [self.x, self.y]
        cv2.imshow('Spline', canvas)
        cv2.setMouseCallback('Spline', self.mousedrag)

    def mousedrag(self, event, x, y, flags, param):
        global canvas, radius

        if event == cv2.EVENT_MOUSEMOVE and \
                (x <= self.x + radius) and \
                (x >= self.x - radius) and \
                (y <= self.y + radius) and \
                (y >= self.y - radius):
            self.h = True
            print("close")
        if event == cv2.EVENT_LBUTTONDOWN and \
                (x <= self.x + radius) and \
                (x >= self.x - radius) and \
                (y <= self.y + radius) and \
                (y >= self.y - radius):
            print("down")
            self.h = True
            canvas = cv2.circle(canvas, self.pt, 10, (0, 255, 255), -1, lineType=cv2.LINE_AA)
        elif event == cv2.EVENT_LBUTTONUP:
            self.h = False
            print(self.pt)
            print("up")
        if self.h:
            print(self.pt)
            self.pt = [x, y]

# Canvas Params
height = 512
width = 512
canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = [int(width/2), int(height/2)]

# Initial Points for Handles

radius = 2
p0 = Handle(0, -150)#np.array([0, -150]) + origin
p1 = Handle(-224, 200)#np.array([-224, 200]) + origin
p2 = Handle(192, 0)#np.array([192, 0]) + origin
p3 = Handle(232, 192)#np.array([232, 192]) + origin

#p0.h = False
#p1.h = False
#p2.h = False
#p3.h = False

while True:
    # Clear Canvas
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Spline Functions
    t = .05
    lp0 = lerp(p0.pt, p1.pt, t)
    lp1 = lerp(p3.pt, p2.pt, t)
    spline = lerp_spline(lp0, lp1)

    # Draw Spline
    canvas = cv2.polylines(canvas, [spline], False, (255, 255, 0), 1, lineType=cv2.LINE_AA)

    # Draw Handles
    canvas = cv2.circle(canvas, lp0[0], 2, (255, 0, 0), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp1[0], 2, (255, 255, 0), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp0[-1], 2, (0, 255, 255), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp1[-1], 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)
    canvas = cv2.line(canvas, p0.pt, p1.pt, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    canvas = cv2.line(canvas, p2.pt, p3.pt, (255, 255, 255), 1, lineType=cv2.LINE_AA)


    cv2.imshow('Spline', canvas)
    #cv2.setMouseCallback('Spline', Handle.mouse_drag)
    cv2.waitKey(1)