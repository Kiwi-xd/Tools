import numpy as np
import cv2
import imutils


def registration(img1, img2):   # img1为原始图像，img2为待配准图像
    def sift_kp(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d_SIFT.create()
        kp, des = sift.detectAndCompute(image, None)
        kp_image = cv2.drawKeypoints(gray_image, kp, None)
        return kp_image, kp, des

    def get_good_match(des1, des2):
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        return good, matches

    def siftImageAlignment(img1, img2):
        f1, kp1, des1 = sift_kp(img1)
        f2, kp2, des2 = sift_kp(img2)
        goodMatch, matches = get_good_match(des1, des2)

        # # 显示特征点以及连接
        # cv2.namedWindow('feature1', cv2.WINDOW_NORMAL)
        # cv2.namedWindow('feature2', cv2.WINDOW_NORMAL)
        # cv2.imshow('feature1', f1)
        # cv2.imshow('feature2', f2)
        # match_img = cv2.drawMatches(img1, kp1, img2, kp2, goodMatch, None, flags=2)
        # cv2.imshow('match', match_img)
        # cv2.waitKey(0)
        # # 显示end

        if len(goodMatch) > 4:
            ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            ransacReprojThreshold = 4
            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold);
            # 其中H为求得的单应性矩阵矩阵
            # status则返回一个列表来表征匹配成功的特征点。
            # ptsA,ptsB为关键点
            # cv2.RANSAC, ransacReprojThreshold这两个参数与RANSAC有关
            imgOut = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
                                         flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        return imgOut, H, status
    result, _, _ = siftImageAlignment(img1, img2)
    allImg = np.concatenate((img1, img2, result), axis=1)
    return result


def main():
    img1 = cv2.imread('./imgs/rgb/Lena.bmp')
    img2 = cv2.imread('./imgs/rgb/Lena.bmp')

    # 旋转构建浮动图像
    img2 = imutils.rotate(img2, 30)

    # 补充实验1
    img2 = cv2.resize(img2,  None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    row, col = img2.shape[:2]
    bottom = img2[row - 2:row, 0:col]
    mean = cv2.mean(bottom)[0]
    bordersize = 64
    img2 = cv2.copyMakeBorder(
        img2,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )
    # 补充实验end

    while img1.shape[0] > 1000 or img1.shape[1] > 1000:
        img1 = cv2.resize(img1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    while img2.shape[0] > 1000 or img2.shape[1] > 1000:
        img2 = cv2.resize(img2, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    result = registration(img1, img2)
    cv2.namedWindow('1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    cv2.imshow('1', img1)
    cv2.imshow('2', img2)
    cv2.imshow('Result', result)

    # cv2.imshow('Result',allImg)
    # if cv2.waitKey(2000) & 0xff == ord('q'):
    #     cv2.destroyAllWindows()
    cv2.waitKey(0)

main()
