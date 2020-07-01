import cv2
import numpy as np

img1 = cv2.imread('5.png')
img = cv2.resize(img1,(488,145),interpolation=cv2.INTER_AREA)
cv2.imshow('image1', img)#将归一化的图片显示

# 将图像转为灰度图
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('image2', img)#显示灰度图

#高斯去噪
img = cv2.GaussianBlur(img, (9, 9), 0)
cv2.imshow('image3', img)#图片显示

#二值化
ret, thresh1 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)

white = []  # 记录每一列的白色像素总和
black = []  # ..........黑色.......
height = thresh1.shape[0]
width = thresh1.shape[1]
white_max = 0
black_max = 0
# 计算每一列的黑白色像素总和
for i in range(width):
    s = 0  # 这一列白色总数
    t = 0  # 这一列黑色总数
    for j in range(height):
        if thresh1[j][i] == 255:
            s += 1
        if thresh1[j][i] == 0:
            t += 1
    white_max = max(white_max, s)
    black_max = max(black_max, t)
    white.append(s)
    black.append(t)
    # print(s)
    # print(t)

arg = False  # False表示白底黑字；True表示黑底白字
if black_max > white_max:
    arg = True
# cv2.imshow('image4', img)

# 反色
def inverse_color(edged):
    height, width = edged.shape
    img2 = edged.copy()
    for i in range(height):
        for j in range(width):
            img2[i, j] = (255 - edged[i, j])
    return img2

if arg:
    img = inverse_color(img)

cv2.imshow('image5', img)
cv2.waitKey(0)
# 垂直投影

#二值化
ret, thresh1 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
(h, w) = thresh1.shape  # 返回高和宽
# 初始化一个跟图像宽一样长度的数组，用于记录每一列的黑点个数
a = [0 for z in range(0, w)]
black_max1 = 0
white_max1 = 0
for j in range(0, w):  # 遍历每一列
    for i in range(0, h):  # 遍历每一行
        if thresh1[i, j] == 0:  # 判断该点是否为黑点，0代表是黑点
            a[j] += 1# 该列的计数器加1
            black_max1 +=1
            thresh1[i, j] = 255  # 记录完后将其变为白色，即等于255
        else:
            white_max1 +=1

for j in range(0, w):  # 遍历每一列
    for i in range(h - a[j], h):  # 从该列应该变黑的最顶部的开始向最底部设为黑点
        # for i in range(0,a[i]):
        thresh1[i, j] = 0  # 设为黑点
cv2.imshow('image6', thresh1)

# 矩形分割字符
image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
blue = (255, 0, 0)

# 分割图像
def find_end(start_):
    end_ = start_ + 1
    for m in range(start_ + 1, width - 1):
        if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
            end_ = m
            break
    return end_

n = 1
start = 1
end = 2
while n < width - 2:
    n += 1
    if (white[n] if arg else black[n]) > (0.05 * white_max if arg else 0.05 * black_max):# 上面这些判断用来辨别是白底黑字还是黑底白字0.05这个参数请多调整，对应上面的0.95
        start = n
        end = find_end(start)
        n = end
        if end - start > 5:
            cj = image[1:height, start:end]
            cv2.imshow('image7', cj)
            image7 = cv2.rectangle(image, (start, 10), (end, 140), blue, 2)
            cv2.waitKey(0)

cv2.imshow('image8',image7)
cv2.waitKey(0)
