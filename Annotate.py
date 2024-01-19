import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Initialize the list to store coordinates
coordinates = []

def onclick(event):
    # Store the coordinates of the clicked point
    ix, iy = event.xdata, event.ydata
    print('x = %d, y = %d' % (ix, iy))

    # Append to the list of coordinates
    coordinates.append((ix, iy))

    # Optionally, you can annotate the point on the image itself
    plt.gca().annotate(len(coordinates), (ix, iy), color='red', weight='bold')

    plt.draw()

# Load and show the image
image_path = 'data/d1_ex2.png'
image = mpimg.imread(image_path)
fig, ax = plt.subplots()
ax.imshow(image)

# Connect the click event to the onclick function
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

# Print or save the coordinates to a file
print(coordinates)

with open('annotations.txt', 'w') as file:
    for coord in coordinates:
        file.write('%d,%d\n' % coord)