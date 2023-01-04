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


# Drag and drop handles
def mouse_click(event, x, y, flags, param):
    global p0, p1, p2, p3, h0, h1, h2, h3, canvas, radius
    if event == cv2.EVENT_LBUTTONDOWN and \
            (x <= p0[0] + radius) and \
            (x >= p0[0] - radius) and \
            (y <= p0[1] + radius) and \
            (y >= p0[1] - radius):
        print("down")
        h0 = True
    elif event == cv2.EVENT_LBUTTONDOWN and \
            (x <= p1[0] + radius) and \
            (x >= p1[0] - radius) and \
            (y <= p1[1] + radius) and \
            (y >= p1[1] - radius):
        print("down")
        h1 = True
    elif event == cv2.EVENT_LBUTTONDOWN and \
            (x <= p2[0] + radius) and \
            (x >= p2[0] - radius) and \
            (y <= p2[1] + radius) and \
            (y >= p2[1] - radius):
        print("down")
        h2 = True
    elif event == cv2.EVENT_LBUTTONDOWN and \
            (x <= p3[0] + radius) and \
            (x >= p3[0] - radius) and \
            (y <= p3[1] + radius) and \
            (y >= p3[1] - radius):
        print("down")
        h3 = True
    elif event == cv2.EVENT_LBUTTONUP:
        h0 = False
        h1 = False
        h2 = False
        h3 = False
    if h0:
        p0 = np.array([x, y])
    if h1:
        p1 = np.array([x, y])
    if h2:
        p2 = np.array([x, y])
    if h3:
        p3 = np.array([x, y])


# Canvas Params
height = 512
width = 512
canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = [int(width/2), int(height/2)]

# Initialize Points for Handles
p0 = np.array([0, -150]) + origin
p1 = np.array([-224, 200]) + origin
p2 = np.array([192, 0]) + origin
p3 = np.array([232, 192]) + origin
# Set mouse state defaults and click radius
h0 = False
h1 = False
h2 = False
h3 = False
radius = 5


while True:
    # Clear Canvas
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Spline Functions
    t = .05
    lp0 = lerp(p0, p1, t)
    lp1 = lerp(p3, p2, t)
    spline = lerp_spline(lp0, lp1)

    # Draw Lerp lines
    for i in range(len(lp0)):
        canvas = cv2.line(canvas, lp0[i], lp1[i], (32, 32, 0), 1, lineType=cv2.LINE_AA)
    # Draw Spline
    canvas = cv2.polylines(canvas, [spline], False, (255, 255, 0), 1, lineType=cv2.LINE_AA)

    # Draw Handles
    canvas = cv2.line(canvas, p0, p1, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    canvas = cv2.line(canvas, p2, p3, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp0[0], 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp1[0], 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp0[-1], 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)
    canvas = cv2.circle(canvas, lp1[-1], 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)

    cv2.imshow('Spline', canvas)
    cv2.setMouseCallback('Spline', mouse_click)

    if cv2.waitKey(16) == ord('q'):
        break

cv2.destroyAllWindows()