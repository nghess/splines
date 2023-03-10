import numpy as np
import cv2

# Wave related vars
freqs = 10  # Number of sin and cos frequencies
freq = 1  # Starting frequency
change = 1  # How much freq changes each iteration
loop = 200  # Total points calculated for each wave
sin_waves, cos_waves, cmb_waves = [], [], []  # Empty lists
size = 75  # Window size for each wave

# Canvas
height = (freqs + 1) * size
width = (freqs + 1) * size
canvas = np.zeros((height, width, 3), dtype=np.uint8)


class MakeWave:
    def __init__(self, objlist, function=np.sin, freq=1, steps=loop):
        self.freq = freq
        self.steps = steps
        # Make sin wave
        self.x = np.linspace(0, 2*np.pi*freq, steps)
        self.y = function(self.x)
        objlist.append(self)


class MakeCombo:
    def __init__(self, objlist, sin, cos):
        # Make cosine wave
        self.x = sin.y
        self.y = cos.y
        objlist.append(self)


# Graphics
class Window:
    def __init__(self, objlist, obj, corner=(0, 0), scale=size*.9):
        # Normalize to square, scale and locate
        self.x = (obj.x-np.min(obj.x))/(np.max(obj.x)-np.min(obj.x))
        self.y = (obj.y-np.min(obj.y))/(np.max(obj.y)-np.min(obj.y))
        self.x = np.array([int(x * scale) + corner[0] for x in self.x])
        self.y = np.array([int(y * scale) + corner[1] for y in self.y])
        self.pts = np.column_stack((self.x, self.y))
        # Add to list
        objlist.append(self)

    def draw(self):
        cv2.polylines(canvas, [self.pts], False, (128, 128, 0), 1, lineType=cv2.LINE_AA)


# Create sine and cosine waves
for i in range(freqs):
    sin = MakeWave(sin_waves, function=np.sin, freq=freq)
    cos = MakeWave(cos_waves, function=np.cos, freq=freq)
    freq += change

# Create Combos
for i in range(freqs**2):
    for cos in cos_waves:
        for sin in sin_waves:
            combination = MakeCombo(cmb_waves, cos, sin)

# Sin and Cos windows
sin_windows, cos_windows, cmb_windows = ([], [], [])
for i in range(freqs):
    sin_plt = Window(sin_windows, sin_waves[i], [0, size*(i+1)])
    cos_plt = Window(cos_windows, cos_waves[i], [size*(i+1), 0])

# Combo windows
count, x_loc, y_loc = 0, 0, 0
for y in range(freqs):
    y_loc = size * (y+1)
    for x in range(freqs):
        x_loc = size * (x+1)
        cmb_plt = Window(cmb_windows, cmb_waves[count], [x_loc, y_loc])
        count += 1

# Draw windows
for i in range(freqs):
    sin_windows[i].draw()
    cos_windows[i].draw()
for i in range(freqs**2):
    cmb_windows[i].draw()

# Set beginning of loop
frame = 0

while True:
    # Refresh Background
    background = canvas.copy()

    # Draw points
    for cos in cos_windows:
        background = cv2.circle(background, cos.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    for sin in sin_windows:
        background = cv2.circle(background, sin.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    for cmb in cmb_windows:
        background = cv2.circle(background, cmb.pts[frame], 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)

    # Show Canvas
    cv2.imshow('Spline', background)
    #cv2.imwrite("output/" + str(frame) + "waves.png", background)
    if cv2.waitKey(16) == ord('q'):
        break

    # Looper
    frame += 1
    if frame == loop:
        frame = 0
        #break