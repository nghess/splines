import cv2
import numpy as np

class Circle:
    def __init__(self, x, y, radius, color, thickness=1, lineType=cv2.LINE_AA):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.lineType = lineType
        self.dragging = False

    def draw(self, img):
        cv2.circle(img, (self.x, self.y), self.radius, self.color, self.thickness, self.lineType)

    def on_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if (x - self.x)**2 + (y - self.y)**2 < self.radius**2:
                self.dragging = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.x = x
                self.y = y
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

circles = [Circle(100, 100, 50, (255, 0, 0)), Circle(200, 200, 75, (0, 255, 0))]

cv2.namedWindow('Window')
def on_mouse_event(event, x, y, flags, param):
    for circle in circles:
        circle.on_mouse_event(event, x, y, flags, param)

cv2.setMouseCallback('Window', on_mouse_event)

while True:
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    for circle in circles:
        circle.draw(img)
    cv2.imshow('Window', img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()