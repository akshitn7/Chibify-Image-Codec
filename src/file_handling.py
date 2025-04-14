import cv2

def getFrequencies(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    pixels = img.flatten()
    pixel_freq = {}
    for i in pixels:
        if i not in pixel_freq:
            pixel_freq[i] = 0
        pixel_freq[i] += 1
    return pixel_freq