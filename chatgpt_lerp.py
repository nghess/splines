import cv2
import numpy as np

# Define the starting and ending points of the two lines
start1 = (100, 100)
end1 = (200, 200)
start2 = (300, 100)
end2 = (400, 200)

# Calculate the slope and intercept of the two lines
m1, b1 = np.polyfit((start1[0], end1[0]), (start1[1], end1[1]), 1)
m2, b2 = np.polyfit((start2[0], end2[0]), (start2[1], end2[1]), 1)

# Create an image to draw the lines on
image = np.zeros((300, 500, 3), dtype=np.uint8)

# Draw the two lines on the image
cv2.line(image, start1, end1, (255, 0, 0), 2)
cv2.line(image, start2, end2, (255, 0, 0), 2)

# Create an empty list to store the spline points
spline_points = []

# Use the lerp function to calculate the points on the spline
for t in np.linspace(0, 1, num=20):
    # Calculate the x and y coordinates of the point on the spline
    x = cv2.lerp(start1[0], end1[0], t)
    y = cv2.lerp(start1[1], end1[1], t)

    # Calculate the x and y coordinates of the point on the spline
    x2 = cv2.lerp(start2[0], end2[0], t)
    y2 = cv2.lerp(start2[1], end2[1], t)

    # Calculate the x and y coordinates of the point on the spline
    x3 = cv2.lerp(x, x2, t)
    y3 = cv2.lerp(y, y2, t)

    # Add the point to the list of spline points
    spline_points.append((x3, y3))

# Draw the spline on the image
cv2.polylines(image, [np.int32(spline_points)], isClosed=False, color=(0, 255, 0), thickness=2)

# Display the image
cv2.imshow("Spline", image)
cv2.waitKey(10000)