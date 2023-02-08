import numpy as np
import cv2

# Window size for each wave
size = 50
# Canvas
height = 10 * size
width = 10 * size
canvas = np.zeros((height, width, 3), dtype=np.uint8)
# Points for each wave
loop = 200

class MakeSin:
    def __init__(self, freq=1, steps=loop):
        self.freq = freq
        self.steps = steps
        # Make sin wave
        self.x = np.linspace(0, 2*np.pi*freq, steps)
        self.y = np.sin(self.x)


class MakeCos:
    def __init__(self, freq=1, steps=loop):
        self.freq = freq
        self.steps = steps
        # Make cosine wave
        self.x = np.linspace(0, 2*np.pi*freq, steps)
        self.y = np.cos(self.x)


class MakeCombo:
    def __init__(self, sin, cos):
        # Make cosine wave
        self.x = sin.y
        self.y = cos.y


# Graphics
class Window:
    def __init__(self, object, corner=[0, 0], scale=size*.9):
        self.scale = scale
        self.corner = corner
        self.x = object.x
        self.y = object.y

        # Normalize to square, scale and locate
        self.x = (self.x-np.min(self.x))/(np.max(self.x)-np.min(self.x))
        self.y = (self.y-np.min(self.y))/(np.max(self.y)-np.min(self.y))
        self.x = np.array([int(x * scale) + corner[0] for x in self.x])
        self.y = np.array([int(y * scale) + corner[1] for y in self.y])
        self.pts = np.column_stack((self.x, self.y))

    def draw(self):
        cv2.polylines(canvas, [self.pts], False, (128, 128, 0), 1, lineType=cv2.LINE_AA)


# Create waves
freqs = 9
change = 0
sin_waves, cos_waves, cmb_waves = ([], [], [])

for i in range(freqs):
    sin = MakeSin(freq=change+1)
    cos = MakeCos(freq=change+1)
    sin_waves.append(sin)
    cos_waves.append(cos)
    change += 1

# Create Combos
for i in range(freqs**2):
    for cos in cos_waves:
        for sin in sin_waves:
            combination = MakeCombo(cos, sin)
            cmb_waves.append(combination)

# Sin and Cos windows
sin_windows, cos_windows, cmb_windows = ([], [], [])
for i in range(freqs):
    sin_plt = Window(sin_waves[i], [0, size*(i+1)])
    sin_windows.append(sin_plt)
    cos_plt = Window(cos_waves[i], [size*(i+1), 0])
    cos_windows.append(cos_plt)

# Combo windows
count, x_loc, y_loc = (0, 0, 0)
for y in range(freqs):
    y_loc = size * (y+1)
    for x in range(freqs):
        x_loc = size * (x+1)
        cmb_plt = Window(cmb_waves[count], [x_loc, y_loc])
        cmb_windows.append(cmb_plt)
        count += 1

# Draw windows
for i in range(freqs):
    sin_windows[i].draw()
    cos_windows[i].draw()
for i in range(freqs**2):
    cmb_windows[i].draw()

frame = 0
cv2.imwrite("waves.png", canvas)

while True:

    background = cv2.imread("waves.png")

    for cos in cos_windows:
        background = cv2.circle(background, cos.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    for sin in sin_windows:
        background = cv2.circle(background, sin.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    for cmb in cmb_windows:
        background = cv2.circle(background, cmb.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)

    frame += 1
    if frame == loop:
        frame = 0

    # Show Canvas
    cv2.imshow('Spline', background)
    if cv2.waitKey(16) == ord('q'):
        break
