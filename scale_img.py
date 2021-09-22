import cv2 as cv


def scaleimg(filepath, s, savepath):
    img = cv.imread(filepath)
    w, h = img.shape[:2]
    size = (int(h*s), int(w*s))
    imgscale = cv.resize(img, size, interpolation=cv.INTER_CUBIC)
    cv.imwrite(savepath, imgscale)

if __name__ == '__main__':
    scaleimg('benchmark/benchmark/Thermal/HR/GY.jpg', 0.5, 'benchmark/benchmark/Thermal/LR_bicubic/X2/GYx2.png')
    scaleimg('benchmark/benchmark/Thermal/HR/LL.jpg', 0.5, 'benchmark/benchmark/Thermal/LR_bicubic/X2/LLx2.png')