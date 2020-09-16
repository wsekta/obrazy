import numpy as np
import math


def sort_pairs_by_first(pairs):
    res = []
    while len(pairs):
        min_idx = 0
        for i in range(len(pairs)):
            if pairs[min_idx][0] > pairs[i][0]:
                min_idx = i
        res.append(pairs[min_idx])
        del (pairs[min_idx])
    return res


def line_eq(point1, point2):
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    b = point1[1] - a * point1[0]
    return a, b


def normalize_by_polyline(image, polyline):
    polyline.append((0, 0))
    polyline.append((256, 255))
    polyline = sort_pairs_by_first(polyline)
    res = np.zeros_like(image)
    for i in range(len(polyline) - 1):
        p1, p2 = polyline[i], polyline[i + 1]
        a, b = line_eq(p1, p2)
        res += ((a * image + b)
                * ((image >= p1[0]) & (image < p2[0]))
                ).astype("uint8")
    return res


def calc_hist(src_channel):
    hist = np.zeros(256)
    for i in src_channel:
        hist[i] += 1
    return hist


def entropy(reg):
    if len(reg.shape) == 3:
        hist = (calc_hist(reg[:, :, 0].flatten())
                + calc_hist(reg[:, :, 1].flatten())
                + calc_hist(reg[:, :, 2].flatten())) \
               / (reg.shape[0] * reg.shape[1] * 3)
    else:
        hist = calc_hist(reg.flatten()) / (reg.shape[0] * reg.shape[1])
    hist = list(hist[hist > 0])
    res = -np.sum(np.multiply(np.log(hist), hist))
    return res


def entropy_filter(image, mask_size):
    half_mask_size = mask_size // 2
    height, width = image.shape[:2]
    res = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            low_x = np.max([0, j - half_mask_size])
            up_x = np.min([width, j + half_mask_size])
            low_y = np.max([0, i - half_mask_size])
            up_y = np.min([height, i + half_mask_size])
            reg = image[low_y:up_y, low_x:up_x]
            res[i, j] = entropy(reg)
    min_entropy = min(res.flatten())
    max_entropy = max(res.flatten())
    res = (res - min_entropy) / (max_entropy - min_entropy) * 255
    res = res.astype(np.uint8)
    return res


def linear_se(length, angle):
    theta = math.radians(angle)
    dx = abs(math.cos(theta))
    dy = abs(math.sin(theta))
    lgx = length * dx
    n2x = round((lgx - 1) / 2)
    nx = 2 * n2x + 1
    lgy = length * dy
    n2y = round((lgy - 1) / 2)
    ny = 2 * n2y + 1
    res = np.zeros([ny, nx])
    if math.cos(theta) >= 0:
        points = line(0, ny - 1, nx - 1, 0)
    else:
        points = line(nx - 1, ny - 1, 0, 0)
    for x in points:
        res[x[1], x[0]] = 1
    return res


def line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    y_step = 1 if y1 < y2 else -1
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += y_step
            error += dx
    if swapped:
        points.reverse()
    return points


def erode(image, se):
    res = np.zeros_like(image)
    width, height = image.shape[:2]
    mask_x, mask_y = se.shape[:2]
    half_mask_x = mask_x // 2
    half_mask_y = mask_y // 2
    for x in range(math.ceil(mask_x / 2), width - mask_x // 2):
        for y in range(math.ceil(mask_y / 2), height - half_mask_y):
            on = image[x - half_mask_x:x + half_mask_x + 1, y - half_mask_y: y + half_mask_y + 1]
            res[x, y] = min(on[(se == 1)])
    return res


def dilate(image, se):
    res = np.zeros_like(image)
    width, height = image.shape[:2]
    mask_x, mask_y = se.shape[:2]
    half_mask_x = mask_x // 2
    half_mask_y = mask_y // 2
    for x in range(math.ceil(mask_x / 2), width - mask_x // 2):
        for y in range(math.ceil(mask_y / 2), height - half_mask_y):
            on = image[x - half_mask_x:x + half_mask_x + 1, y - half_mask_y: y + half_mask_y + 1]
            res[x, y] = max(on[(se == 1)])
    return res


def imopen(image, se_length, se_angle):
    se = linear_se(se_length, se_angle)
    return dilate(erode(image, se), se)


def hit_miss(image, se):
    true_mask = se * (se == 1)
    false_mask = se * (se == -1) * -1
    res = erode(image, true_mask) & erode(~image, false_mask)
    return res


def convex_hull(src_image):
    se_1 = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
    se_2 = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)
    compare = np.zeros_like(src_image)
    res = src_image
    while not np.array_equal(res, compare):
        compare = res
        for i in range(4):
            res = res | hit_miss(res, se_1)
            res = res | hit_miss(res, se_2)
            se_1 = np.rot90(se_1)
            se_2 = np.rot90(se_2)
    return res
