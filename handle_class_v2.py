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


# Lists for lerps and splines
lerp_lines = []
segments = []


def create_spline():
    # Lerp handles build guide rails
    for l in range(1, len(handles)):
        # Toggle direction of each lerp
        if l % 2 == 0:
            line = lerp(handles[l].arm1, handles[l].knot, .05)
            lerp_lines.append(line)
            line = lerp(handles[l-1].knot, handles[l-1].arm1, .05)
            lerp_lines.append(line)
        else:
            line = lerp(handles[l].arm2, handles[l].knot, .05)
            lerp_lines.append(line)
            line = lerp(handles[l-1].knot, handles[l-1].arm2, .05)
            lerp_lines.append(line)
    # Lerp spline along guide rails
    for s in range(0, len(lerp_lines)-1, 2):
        segment = lerp_spline(lerp_lines[s], lerp_lines[s+1])
        segments.append(segment)


def on_mouse_event(event, x, y, flags, param):
    add_handle(event, x, y, flags, param)
    for handle in handles:
        handle.drag_and_drop(event, x, y, flags, param)


def add_handle(event, x, y, flags, param):
    if event == cv2.EVENT_RBUTTONDOWN:
        Handle(x-origin[0], y-origin[1])


class Handle:
    def __init__(self, x, y):
        # Mouse location and mouse event related params
        self.x = x + origin[0]
        self.y = y + origin[1]
        self.knot_drag = False
        self.arm1_drag = False
        self.arm2_drag = False
        self.radius = 5
        # Handle points
        self.knot = np.array([self.x, self.y])
        self.arm1 = np.array([self.x, self.y + 100])
        self.arm2 = np.array([self.x, self.y - 100])
        # Add new handle to list
        global handles
        handles.append(self)

    def draw_handle(self, img, brightness, idx):
        cv2.line(img, self.arm1, self.arm2, (255, 255, 255), 1, lineType=cv2.LINE_AA)
        cv2.circle(img, self.knot, 3, (0, 0, brightness), -1, lineType=cv2.LINE_AA)
        cv2.circle(img, self.arm1, 3, (0, 0, brightness), -1, lineType=cv2.LINE_AA)
        cv2.circle(img, self.arm2, 3, (0, 0, brightness), -1, lineType=cv2.LINE_AA)
        #cv2.putText(img, f"{self.knot} idx={idx}", self.knot+10, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.3, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

    def drag_and_drop(self, event, x, y, flags, param):
        global datum  # Drag starting point
        # On left click, check if mouse is within click radius of a handle or knot
        if event == cv2.EVENT_LBUTTONDOWN:
            datum = np.array([x, y])  # Get initial mouse position
            if (x - self.knot[0])**2 + (y - self.knot[1])**2 <= self.radius**2:
                self.knot_drag = True
            elif (x - self.arm1[0])**2 + (y - self.arm1[1])**2 <= self.radius**2:
                self.arm1_drag = True
            elif (x - self.arm2[0])**2 + (y - self.arm2[1])**2 <= self.radius**2:
                self.arm2_drag = True
        # Possible drag and drops
        elif event == cv2.EVENT_MOUSEMOVE:
            # Drag knot
            if self.knot_drag:
                mouse = np.array([x, y])
                change = (mouse - datum)
                self.knot = mouse
                self.arm1 = self.arm1 + change
                self.arm2 = self.arm2 + change
                datum = np.array([x, y])  # Update mouse position
            # Drag arm 1
            elif self.arm1_drag:
                self.arm1 = np.array([x, y])
                arm_offset = self.knot - self.arm1  # Distance between handle and knot
                self.arm2 = self.knot + arm_offset  # Opposite arm gets offset
            # Drag arm 2
            elif self.arm2_drag:
                self.arm2 = np.array([x, y])
                arm_offset = self.knot - self.arm2  # Distance between handle and knot
                self.arm1 = self.knot + arm_offset  # Opposite arm gets offset
        # Mouse up
        elif event == cv2.EVENT_LBUTTONUP:
            self.knot_drag = False
            self.arm1_drag = False
            self.arm2_drag = False


# Canvas Params
height = 800
width = 1600
canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = np.array([int(width/2), int(height/2)])

# List to store handles as they are created
handles = []
# Frame count
i = 0

while True:
    # Wipe canvas each frame
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    # Handle Count
    c = 0

    # Create spline
    lerp_lines = []
    segments = []
    create_spline()

    # Draw lerp lines
    for l in range(0, len(lerp_lines)-1, 2):
        for pt in range(len(lerp_lines[0])):
            canvas = cv2.line(canvas, lerp_lines[l][pt], lerp_lines[l+1][pt], (32, 32, 0), 1, lineType=cv2.LINE_AA)

    # Draw spline segments
    for s in segments:
        canvas = cv2.polylines(canvas, [s], False, (255, 255, 0), 1, lineType=cv2.LINE_AA)

    # Draw Handle points
    for handle in handles:
        fade = int((c/len(handles))*205)
        handle.draw_handle(canvas, brightness=fade+50, idx=c)
        c += 1

    # Show Canvas
    cv2.imshow('Spline', canvas)
    cv2.setMouseCallback('Spline', on_mouse_event)
    #cv2.imwrite("output/" + str(i) + "lerp.png", canvas)
    i += 1
    if cv2.waitKey(16) == ord('q'):
        break
