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

def on_mouse_event(event, x, y, flags, param):
    for handle in handles:
        handle.drag_and_drop(event, x, y, flags, param)

class Handle:
    def __init__(self, x, y):
        self.dragging = False
        self.x = x + origin[0]
        self.y = y + origin[1]
        self.pt = [self.x, self.y]
        self.radius = 5

    def draw(self, img):
        cv2.circle(img, self.pt, 3, (0, 0, 255), -1, lineType=cv2.LINE_AA)

    def drag_and_drop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if (x - self.x)**2 + (y - self.y)**2 < self.radius**2:
                self.dragging = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.x = x
                self.y = y
                self.pt = [x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

# Canvas Params
height = 512
width = 512
canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = [int(width/2), int(height/2)]

# Initial Points for Handles
p0 = Handle(0, -150)
p1 = Handle(-224, 200)
p2 = Handle(192, 0)
p3 = Handle(232, 192)
# Handles list for mouse events
handles = [p0, p1, p2, p3]

while True:
    # Wipe canvas each frame
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Spline Functions
    t = .05
    lp0 = lerp(p0.pt, p1.pt, t)
    lp1 = lerp(p3.pt, p2.pt, t)
    spline = lerp_spline(lp0, lp1)

    # Draw Lerp lines
    for i in range(len(lp0)):
        canvas = cv2.line(canvas, lp0[i], lp1[i], (32, 32, 0), 1, lineType=cv2.LINE_AA)
    # Draw Spline
    canvas = cv2.polylines(canvas, [spline], False, (255, 255, 0), 1, lineType=cv2.LINE_AA)

    # Draw Handles
    canvas = cv2.line(canvas, p0.pt, p1.pt, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    canvas = cv2.line(canvas, p2.pt, p3.pt, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    for handle in handles:
        handle.draw(canvas)

    # Show Canvas
    cv2.imshow('Spline', canvas)
    cv2.setMouseCallback('Spline', on_mouse_event)
    if cv2.waitKey(16) == ord('q'):
        break

cv2.destroyAllWindows()
