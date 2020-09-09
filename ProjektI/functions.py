import numpy as np


def SE_lin(length: float, deg: float) -> np.ndarray:
    deg = np.pi * deg / 180.0
    x = int(np.floor(abs(length * np.cos(deg))))
    y = int(np.floor(abs(length * np.sin(deg))))
    if x == 0 or x == 1:
        return np.ones((length, 1)).astype(int)
    if y == 0 or y == 1:
        return np.ones((1, length)).astype(int)
    if x % 2 == 0:
        x += 1
    if y % 2 == 0:
        y += 1
    tab = np.array([[0 for i in range(x + 1)] for j in range(y + 1)])
    iterator = 0
    if x > y:
        for i in range(x + 1):
            tab[int(round(iterator))][i] = 1
            iterator += y / x
    else:
        for j in range(y + 1):
            tab[j][int(round(iterator))] = 1
            iterator += x / y

    if np.tan(deg) > 0:
        return tab[::-1, :]
    return tab


import math


def erode(src_image, se):
    result_image = np.zeros_like(src_image)
    img_width, img_height = src_image.shape[:2]
    mask_x, mask_y = se.shape[:2]
    mask_half_x = math.floor(mask_x / 2)
    mask_half_y = math.floor(mask_y / 2)
    for i in range(math.ceil(mask_x / 2), img_width - math.floor(mask_x / 2)):
        for j in range(math.ceil(mask_y / 2), img_height - mask_half_y):
            on = src_image[i - mask_half_x:i + mask_half_x, j - mask_half_y: j + mask_half_y]
            bool_idx = (se == 1)
            result_image[i, j] = on[bool_idx].min()

    return result_image


def dilate(image: np.ndarray, SE: np.ndarray) -> np.ndarray:
    res = np.zeros((image.shape[0] + SE.shape[0], image.shape[1] + SE.shape[1]))
    for y in range(image.shape[1]):
        for x in range(image.shape[0]):
            res[x:x + SE.shape[0], y:y + SE.shape[1]] = np.maximum(res[x:x + SE.shape[0], y:y + SE.shape[1]],
                                                                   image[x, y] * SE)

    return res[SE.shape[0] // 2 + 1:SE.shape[0] // 2 + image.shape[0] + 1,
           SE.shape[1] // 2 + 1:SE.shape[1] // 2 + image.shape[1] + 1]


def imopen(image: np.ndarray, SE: np.ndarray) -> np.ndarray:
    return dilate(erode(image, SE), SE)


def convex_hull(src_image: np.ndarray):
    # Create structural elements
    src_image = src_image.astype(bool)
    se_0deg = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
    se_45deg = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)

    # Allocate comparison image to enter while
    compare = np.zeros_like(src_image)
    result_image = src_image

    # Perform hit-or-miss until no change
    while not np.array_equal(result_image, compare):
        compare = result_image

        # Hit-or-miss for each se position
        for i in range(4):
            result_image = result_image | hit_miss(result_image, se_0deg)
            result_image = result_image | hit_miss(result_image, se_45deg)
            se_0deg = np.rot90(se_0deg)
            se_45deg = np.rot90(se_45deg)

    return result_image


def hit_miss(src_image, se):
    # Create mask [0, 1] from [-1, 0, 1]
    true_mask = se * (se == 1)
    false_mask = se * (se == -1) * -1

    # Perform two erosion to get hit-or-miss
    result_image = erode(src_image, true_mask) & erode(~src_image, false_mask)

    return result_image
