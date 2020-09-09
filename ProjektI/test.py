from functions import *
from matplotlib import image
from matplotlib import pyplot
from skimage.morphology import convex_hull_image

image = image.imread('wklensla.png')
# image =  image.astype(int) / (-255) + 1
# image = image[:,:,1]

# image = (1 - image/255).astype(bool)

# pyplot.imshow(image)
# pyplot.show()
# print(dilate(image, SE_lin(10, 45)).shape)

# pyplot.imshow(imopen(image, SE_lin(10, 30)), cmap="Greys_r")

pyplot.imshow(dilate(image, SE_lin(15, 30)), cmap="Greys_r")

pyplot.show()
