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
    create_handle(event, x, y, flags, param)
    for handle in handles:
        handle.drag_and_drop(event, x, y, flags, param)

class Handle:
    def __init__(self, x, y):
        self.dragging = False
        self.x = x + origin[0]
        self.y = y + origin[1]
        self.pt = [self.x, self.y]
        self.radius = 5
        global handles
        handles.append(self)

    def draw_pt(self, img, brightness):
        cv2.circle(img, self.pt, 3, (0, 0, brightness), -1, lineType=cv2.LINE_AA)
        cv2.putText(img, f"{self.pt[0]}, {self.pt[1]}", np.asarray(self.pt)+10, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.3, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

    def drag_and_drop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if (x - self.x)**2 + (y - self.y)**2 <= self.radius**2:
                self.dragging = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.x = x
                self.y = y
                self.pt = [x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False



def create_handle(event, x, y, flags, param):
    global handles
    global lerp_lines
    global segments
    if event == cv2.EVENT_RBUTTONDOWN:
        # Find distance between last two handles
        difference = np.asarray(handles[-1].pt) - np.asarray(handles[-2].pt)
        # Add distance for mirrored handle
        handle_n1 = difference + np.asarray(handles[-1].pt)
        # Create mirrored handle
        Handle(handle_n1[0]-origin[0], handle_n1[1]-origin[1])
        # Duplicate knot handle
        handles.insert(-2, handles[-2])
        # Add base handle for new segment
        Handle(x-origin[0], y-origin[1])
        # Add tail handle for new segment
        new_tail = difference + np.asarray(handles[-1].pt)
        Handle(new_tail[0]-origin[0], new_tail[1]-origin[1])

        # List to store lerp lines as they are created
        lerp_lines = []
        # List to store spline segments as they are created
        segments = []

        # Create handle lines and splines from handles
        create_spline()

def create_spline():
    for l in range(0, len(handles), 2):
        line = lerp(handles[l].pt, handles[l+1].pt, .05)
        lerp_lines.append(line)
    for s in range(0, len(lerp_lines), 2):
        segment = lerp_spline(lerp_lines[s], lerp_lines[s+1])
        segments.append(segment)


# Canvas Params
height = 800
width = 1600
canvas = np.zeros((height, width, 3), dtype=np.uint8)
origin = [int(width/2), int(height/2)]

# List to store handles as they are created
handles = []
# Initial Points for Handles
p0 = Handle(0, -150)
p1 = Handle(-224, 200)
p2 = Handle(192, 0)
p3 = Handle(232, 192)

while True:
#for i in range(1):
    # List to store lerp lines as they are created
    lerp_lines = []
    # List to store spline segments as they are created
    segments = []

    # Create handle lines and splines from handles
    create_spline()
    # Wipe canvas each frame
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    c = 0

    # Draw Spline
    for s in segments:
        canvas = cv2.polylines(canvas, [s], False, (255, 255, 0), 1, lineType=cv2.LINE_AA)


    # Draw lerp lines
    for l in range(len(lerp_lines) // 2):
        for pt in range(len(lerp_lines[0])):
            canvas = cv2.line(canvas, lerp_lines[l][pt], lerp_lines[l+1][pt], (32, 32, 0), 1, lineType=cv2.LINE_AA)

    # Draw Handle lines
    for h in range(1, len(handles), 2):
        canvas = cv2.line(canvas, handles[h].pt, handles[h-1].pt, (255, 255, 255), 1, lineType=cv2.LINE_AA)

    # Draw Handle points
    for handle in handles:
        fade = int((c/len(handles))*205)
        handle.draw_pt(canvas, brightness=fade+50)
        c += 1

    # Show Canvas
    cv2.imshow('Spline', canvas)
    cv2.setMouseCallback('Spline', on_mouse_event)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
