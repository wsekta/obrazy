from functions import *
from matplotlib import image
from matplotlib import pyplot
from skimage.morphology import convex_hull_image

# img = image.imread('wklensla.png')
# img = (img / 255).astype(bool)
# img = 255 * (~ img).astype("uint8")
# image.imsave('wklensla.png', img)
# image = image.imread('peppers.jpg')
# image = image.imread('cameraman.bmp')
# pyplot.imshow(image, cmap="Greys_r")
# print(sort_pairs_by_first([(50,10),(40,5),(90,99),(60,20),(30,1)]))
# pyplot.imshow(normalize_by_polyline(image,[(50,100),(150,150),(200,250)]), cmap="Greys_r")

# print(f"entropy before filter {entropy(image)}")
# im_filt = entropy_filter(image, 5)
"""pyplot.imshow(im_filt, cmap="Greys_r")
print(f"entropy before filter {entropy(im_filt)}")"""

# pyplot.imshow(dilate(image, liner_se(10, 45)), cmap="Greys_r")
# pyplot.imshow(erode(image, liner_se(10, 45)), cmap="Greys_r")

# pyplot.imshow(imopen(image, 15, 30), cmap="Greys_r")

# pyplot.imshow(convex_hull(image), cmap="Greys_r")

bulb = image.imread('wklensla.png')
bulb = (bulb / 255).astype("bool")
pyplot.imshow(imopen(bulb, 9, 30), cmap="Greys_r")
pyplot.show()
