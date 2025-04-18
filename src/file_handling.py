import cv2

def get_pixels(filepath):
    img = cv2.imread(filepath, 0)
    pixels = img.flatten()
    return pixels, img.shape

def get_frequencies(pixels):
    pixel_freq = {}
    for i in pixels:
        if i not in pixel_freq:
            pixel_freq[i] = 0
        pixel_freq[i] += 1
    return pixel_freq

