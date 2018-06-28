from __future__ import print_function
import os
import sys
import cv2
import numpy as np

# 从文件目录中读取几百张图片
def readImages(path):
	print('从这儿读图片呢 ' + path, end='...')
	# 存储图像.
	images = []
	# 列出目录中的所有文件并逐个从文件中读取
	for filePath in sorted(os.listdir(path)):
		fileExt = os.path.splitext(filePath)[1]
		if fileExt in ['.jpg', '.jpeg','.png']:#如果后缀是jpg，jpeg，png
			# 将图片文件放进去
			imagePath = os.path.join(path, filePath)
			im = cv2.imread(imagePath)#再读文件

			if im is None :#如果没文件
				print('image:{} not read properly'.format(imagePath))
			else :
				# 将图片转换成浮点数
				im = np.float32(im)/255.0
				# 将图片加到im里去
				images.append(im)
				# 水平旋转图片，数据集*2，让最后的效果更左右对称
				imFlip = cv2.flip(im, 1);
				# 将图片加到im里去
				images.append(imFlip)
	tupianshu = len(images) / 2#实际图片数量为
	# 如果没读进去图片，就退出
	if tupianshu == 0 :
		print('没看到图片啊，智障')
		sys.exit(0)#退出
		print(str(tupianshu) + ' 张图片读到了.')
	return images#返回文件

def createDataMatrix(images):#这里的images就是上一个函数返回的
	# 把几百张图片变成一个大矩阵
	# 每张图片大小必须一样
	#( w * h * 3, tupianshu )
	# w = 图片的长
	# h = 图片的宽
	# 3 是rgb三通道
	print('正在从图片变成矩阵',end=' ... ')
	tupianshu = len(images)#tupianshu 图片数
	size = images[0].shape#图片大小
	dajuzhen = np.zeros((tupianshu, size[0] * size[1] * size[2]), dtype=np.float32)#先搞一个全是零的数组，大小正确
	for i in range(0, tupianshu):
		image = images[i].flatten()#把每张图片压平
		dajuzhen[i,:] = image#导入到图片里
	print('我好了')
	return dajuzhen#大矩阵 返回



def eigenFace(dirName='images'):

    bar_nums = 10#最后显示出来能滑动的bar有几个
    bar_values = 255#每个能滑动的bar上的值有几个
    shujuji = 'nba_bianhuan_resize'#图片集的路径
    images = readImages(shujuji)# 读图片
    size = images[0].shape#图片的大小
    dajuzhen = createDataMatrix(images)#搞出大矩阵
    print('在算PCA,别急 ', end='...')
    #用opencv自带的搞出平均向量和特征向量
    mean, eigenVectors = cv2.PCACompute(dajuzhen, mean=None, maxComponents=bar_nums)
    print ('我好了')
    averageFace = mean.reshape(size)#把压平的矩阵变回图片大小矩阵
    eigenFaces = [];
    for eigenVector in eigenVectors:
        eigenFace = eigenVector.reshape(size)
        eigenFaces.append(eigenFace)


# 将权重脸（weighted eigen face）加到平均脸（mean face）
    def createNewFace(*args):
        output=averageFace
        for i in range(0, bar_nums):
            # 产生opencv界面
            sliderValues[i] = cv2.getTrackbarPos('Weight' + str(i), 'Trackbars');
            # 每个bar上的值不能为负 opencv规定的
            # 所以我们这么定义weight
            weight = sliderValues[i] - bar_values / 2
            # 结果是特征脸乘以权重+平均脸
            output = np.add(output, eigenFaces[i] * weight)
        # 产生opencv界面
        output = cv2.resize(output, (0, 0), fx=2, fy=2)
        cv2.imshow('Result', output)


    def resetSliderValues(*args):
        # 只要鼠标点一下opencv图片界面，就将bar的weight都调到初始值
        for i in range(0, bar_nums):
            cv2.setTrackbarPos('Weight' + str(i), 'Trackbars', int(bar_values / 2));  # 注意bar_values/2必须是整数，不然报错
        createNewFace()


    #创建opencv的图像结果界面
    cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
    output = cv2.resize(averageFace, (0,0), fx=2, fy=2)
    cv2.imshow('Result', output)
    #创建opencv的bar结果界面
    cv2.namedWindow('Trackbars', cv2.WINDOW_AUTOSIZE)
    sliderValues = []
    # 创建能拖动的bar
    for i in range(0, bar_nums):
        sliderValues.append(bar_values/2)
        cv2.createTrackbar( 'Weight' + str(i), 'Trackbars', int(bar_values/2), bar_values, createNewFace)#注意bar_values/2必须是整数，不然报错
    #只要鼠标点一下opencv图片界面，就将bar的weight都调到初始值
    cv2.setMouseCallback('Result', resetSliderValues);

    print('''Usage:
        使用滑块更改权重
        点击结果窗口重置滑块
        按ESC键结束程序。''')

    cv2.waitKey(0)
    cv2.destroyAllWindows()
