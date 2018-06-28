import numpy as np
import cv2
import sys
import requests
import os
import re
import imageio
from json import JSONDecoder
from scipy.spatial import Delaunay
from PIL import Image


def detect(img_path,key,secret):

    """
    把FACE++识别人脸识别功能封装为一个函数
    :param img_path: 图片文件，最好放在与该文件相同的文件夹目录下
    :param key: API的公钥
    :param secret: API的密钥
    :return: 返回一个人脸识别点的字典
    """
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"

    # data中 return_landmark:2  返回106个点  1 返回83个点
    data = {"api_key":
                key, "api_secret": secret, "return_landmark": "2", 'return_attributes': 'none'}
    files = {"image_file":
                 open(img_path, "rb")}
    response = requests.post(http_url,
                             data=data, files=files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    landmarks = req_dict['faces'][0]['landmark']
    new_dict = {}
    # 保存到txt中，方便留底与后续处理
    with open("result_%s.txt" % img_path, 'w+') as f:
        for k, v in landmarks.items():
            new_dict[k] = np.array([v['x'], v['y']])

    return new_dict


def addBorderPoints(points, img):
    """
    该函数功能是给处理图片准备要划分三角形的时候，
    把图片四个顶点和四条边的中点的坐标添加到带划分的点中
    这让得劳内三角形才能完整的划分整张图片，详见报告中得劳内三角形的图

    :param points: 该图片人脸识别出来的特征点
    :param img: 该图片的图片数组
    :return: 添加完边界点后的所有点
    """
    #一个列表存储结果
    pointsList = []
    #先把所有face++识别出来的点加到这个列表当中
    for point in points:
        pointsList.append((int(point[0]), int(point[1])))
    #得到图片尺寸
    y_size, x_size = img.shape[0] - 1, img.shape[1] - 1
    #添加四个顶点和四条边的中点
    pointsList.append((0, int(y_size)))
    pointsList.append((int(x_size), int(y_size)))
    pointsList.append((int(x_size), 0))
    pointsList.append((0, 0))
    pointsList.append((0, int(y_size / 2)))
    pointsList.append((int(x_size / 2), 0))
    pointsList.append((int(x_size / 2), int(y_size)))
    pointsList.append((int(x_size), int(y_size / 2)))

    #返回numpy的数组形式

    return np.array(pointsList)

def delaunaryTriangles(points):
    """
    :param points: 图片的所有要划分的特征点
    :return: 返回所有得劳内三角形三个点对应的点序号

    """
    return Delaunay(points).simplices


def affineTransform(ori, oriTri, dstTri, size):
    """

    :param ori:    #原图像素点
    :param oriTri: #原图三角形
    :param dstTri: #新图对应三角形
    :param size: OPENCV的仿射变换区域使用一个近似于矩形的区域，所以要输入矩形的size
    :return:
    """
    # 分对于对两张图片的一对三角形，寻找代表其对应仿射变换的矩阵
    # 仿射变换的六参数模型
    Matrix = cv2.getAffineTransform(np.float32(oriTri), np.float32(dstTri))

    # 把原图三角形内所有像素仿射到新的图片中
    #
    dst = cv2.warpAffine(ori, Matrix, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT_101)

    return dst


def morphingTriangle(imgs, triList, alpha):
    """
    这个函数是结合两张图片对应的三角形区域来求融合后图片三角区域内的像素
    :param imgs: [oriImg, protoImg, newImg]  一个分别存储着两张原图以及新的融合图片的图片数组
    :param triList: [[pt1,pt2..],[pt1',pt2'..],[pt3''...,pt3''...]]
    :param alpha: 融合度
    :return:
    """
    #由于OPENCV仿射变换区域是矩形，因此我们这里找的是所要做仿射的三角形的最小包围矩形区域
    #用这个包围矩形区域来近似三角形来做仿射

    recs = []  #存储着矩形四个顶点坐标
    recImgs = [] #存储着矩形内所有点像素
    tRects = [[], [], []] #存储着用来近似三角形的矩形

    for i, t in enumerate(triList):
        #求三角形的近似矩形
        recs.append(cv2.boundingRect(np.float32([t])))
        #print(cv2.boundingRect(np.float32([t])))
        #求矩形内的像素
        recImgs.append(imgs[i][recs[i][1]:(recs[i][1] + recs[i][3]), recs[i][0]:(recs[i][0] + recs[i][2])])

        for j in range(3):
            tRects[i].append(((triList[i][j][0] - recs[i][0]), (triList[i][j][1] - recs[i][1])))

    size = (recs[2][2], recs[2][3])
    #对图1对应三角形（实际为矩形）做仿射变换
    affineRec1 = affineTransform(recImgs[0], tRects[0], tRects[2], size)
    #对图2对应三角形（实际为矩形）做仿射变换
    affineRec2 = affineTransform(recImgs[1], tRects[1], tRects[2], size)

    # 通过填充脸部的三角形得到一个mask
    mask = np.zeros((recs[2][3], recs[2][2], imgs[2].shape[2]), dtype=np.float32)
    # fillConvexPoly函数是cv2中用于非凸任意形状填充
    cv2.fillConvexPoly(mask, np.int32(tRects[2]), (1.0, 1.0, 1.0), 16, 0)

    # 计算融合之后的矩形内的像素点
    morphRec = (1 - alpha) * affineRec1 + alpha * affineRec2

    # 得到融合图片的图片数组
    try:
        imgs[2][recs[2][1]:recs[2][1] + recs[2][3], recs[2][0]:recs[2][0] + recs[2][2]] = recImgs[2] * (
                    1 - mask) + mask * morphRec
    except ValueError:
        pass


def morphing(oriImg, protoImg, oriPoints, protoPoints, alpha):
    """

    :param oriImg:第一张图图片数组
    :param protoImg:第二张图图片数组
    :param oriPoints:第一张图特征点
    :param protoPoints:第二张图特征点
    :param alpha: 融合度
    :return:
    """
    #对两张图片的脸部特征点都加上四个顶点与边缘中心点
    oriPoints = addBorderPoints(oriPoints, oriImg)
    protoPoints = addBorderPoints(protoPoints, protoImg)

    #得到融合图片的脸部特征点的坐标
    morphPoints = (1 - alpha) * oriPoints + alpha * protoPoints

    #根据脸部特征点坐标，返回一系列由这些特征点生成的得劳内三角形
    triangleIndList = delaunaryTriangles(morphPoints)

    # 新图片
    newShape = protoImg.shape
    newImg = np.zeros(newShape, dtype=protoImg.dtype)

    for row in newImg:
        for term in row:
            term[2] = 255

    imgs = [oriImg, protoImg, newImg]

    # 对分别对两张原图做对融合图的仿射变换
    for triIndex in triangleIndList:
        tris = [[], [], []]  #存储着每个得劳内三角形三点所对应的特征点的序号（INDEX）
        for i in range(3):
            tris[0].append(np.array(oriPoints[triIndex[i]]))
            tris[1].append(np.array(protoPoints[triIndex[i]]))
            tris[2].append(np.array(morphPoints[triIndex[i]]))
        morphingTriangle(imgs, tris, alpha)
    return imgs[2]


def getPic(ori_path,proto_path,alpha):
    """
    该函数实现融合脸GUI第一个功能，即根据输入的alpha融合度生成一张图片

    :param ori_path:  原图1路径
    :param proto_path:  原图2路径
    :param alpha:  融合度
    :return:
    """

    """
    由于我们发现上传的图片往往包括除了人脸外的下半部分如衣服，融合起来很难看
    该函数功能在于使用CascadeClassifier，这是Opencv中做人脸检测的时候的一个级联分类器
    需要读取已经训练好的保存有特征池的文件
    'haarcascade_frontalface_alt.xml'

    能够实现提取放大图片的人脸并保存到本地的功能
    即我们图像处理的ROI是人脸部分
    """

    path = 'haarcascade_frontalface_alt.xml'
    hc = cv2.CascadeClassifier(path)
    if (hc.empty()):
        print('CascadeClassifer could not be loaded')
        sys.exit()

    oriImg = Image.open(ori_path)
    oriImg = np.array(oriImg)
    protoImg = Image.open(proto_path)
    oriShape = oriImg.shape
    new_protoImg = protoImg.resize((oriShape[1], oriShape[0]), Image.ANTIALIAS)
    new_proto_path = 'Resized_%s' % proto_path
    protoImg = np.array(new_protoImg)
    new_protoImg.save(new_proto_path)

    key1='3o6_lMDRxcpYalXhuXq9cymJeeN7cHCS'
    secret1='6776wZFWYVfYjwDgS8G_0rmWhtXVyUcW'
    key2 = "At0ndsJ0Q5qhEDzViAiQDAi8KJGutPjE"
    secret2 = "cuPyLap40YUkpQHHeXBOuXbpJFXGtoYI"

    #由于API是免费的，所以使用一定次数后会被对方暂时封IP
    #因此用了两套API，使用try..except 结构，当一套暂时失效的时候改用另外一套

    try:
        protoDict = detect(new_proto_path, key2, secret2)
    except KeyError:
        protoDict = detect(new_proto_path, key1, secret1)

    try:
        oriDict = detect(ori_path, key1, secret1)
    except KeyError:
        oriDict = detect(ori_path, key2, secret2)

    #有时候由于图片问题，API无法识别人脸所有部分，导致两张图片识别点个数不同
    #怎么办呢? 下面函数保证两张图片的脸部特征点个数是相同的，即删除了
    #那些只在其中一张图片出现的点
    DeleteList = []
    for key in oriDict:
        if key not in protoDict:
            DeleteList.append(key)
    for key in DeleteList:
        del oriDict[key]

    oriPoints = []
    protoPoints = []

    for key in protoDict:
        protoPoints.append(protoDict[key])
        oriPoints.append(oriDict[key])
    protoPoints = np.array(protoPoints)
    oriPoints = np.array(oriPoints)

    #融合图片
    newImg = morphing(oriImg, protoImg, oriPoints, protoPoints, alpha)
    #提取人脸部分
    faces = hc.detectMultiScale(newImg)
    for face in faces:
        #划定提取人脸部分的大小
        imgROI = newImg[face[1] - 25:face[1] + face[3] + 25,
                 face[0] - 25:face[0] + face[2] + 25]
        img = Image.fromarray(imgROI)
        #保存到本地
        img.resize((500, 500), Image.ANTIALIAS).save("alpha.png")

"""

以下函数利用由20张递增的，不同alpha参数生成的
保存在本地的图片，调用python的imageio库生成一张gif，以在GUI显示

"""


def gen20Pics(ori_path,proto_path):

    """
    该函数与上面那个基本相同，不过是在本地生成20张alpha在0-1成等差数列递增的图片

    :param ori_path: 第一张图路径
    :param proto_path:  第二张图路径
    :return:
    """
    path = 'haarcascade_frontalface_alt.xml'
    hc = cv2.CascadeClassifier(path)
    if (hc.empty()):
        print('CascadeClassifer could not be loaded')
        sys.exit()

    oriImg = Image.open(ori_path)
    oriImg=np.array(oriImg)
    protoImg=Image.open(proto_path)
    oriShape = oriImg.shape
    new_protoImg = protoImg.resize((oriShape[1], oriShape[0]), Image.ANTIALIAS)
    new_proto_path='Resized_%s'%proto_path
    protoImg = np.array(new_protoImg)
    new_protoImg.save(new_proto_path)

    key1='3o6_lMDRxcpYalXhuXq9cymJeeN7cHCS'
    secret1='6776wZFWYVfYjwDgS8G_0rmWhtXVyUcW'
    key2 = "At0ndsJ0Q5qhEDzViAiQDAi8KJGutPjE"
    secret2 = "cuPyLap40YUkpQHHeXBOuXbpJFXGtoYI"

    try :
        protoDict = detect(new_proto_path,key2,secret2)
    except KeyError:
        protoDict = detect(new_proto_path, key1, secret1)

    try:
        oriDict = detect(ori_path, key1, secret1)
    except KeyError:
        oriDict = detect(ori_path, key2, secret2)

    delList = []
    for key in oriDict:
        if key not in protoDict:
            delList.append(key)
    for key in delList:
        del oriDict[key]

    oriPoints = []
    protoPoints = []

    for key in protoDict:
        protoPoints.append(protoDict[key])
        oriPoints.append(oriDict[key])
    protoPoints = np.array(protoPoints)
    oriPoints = np.array(oriPoints)
    alphas=np.linspace(0,1,20)
    for i, alpha in enumerate(alphas):
        newImg = morphing(oriImg, protoImg, oriPoints, protoPoints, alpha)
        faces = hc.detectMultiScale(newImg)
        for face in faces:
             imgROI = newImg[face[1]-25:face[1]+face[3]+25,
                     face[0]-25:face[0]+face[2]+25]
             img=Image.fromarray(imgROI)
             img.resize((500,500),Image.ANTIALIAS).save("%d_result.png" % (i + 1))
        print(str(i) + ' face(s) finished')



def sortKey(s):
    #把生成的本地图片按序号排序，那么生成gif的时候各张图片就是
    #按序号来生成的，不会乱来
    if s:
        try:
            c = re.findall('^\d+', s)[0]
        except:
            c = -1
        return int(c)


def create(image_list, gif_name):

    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    #间隔是0.1s
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.5)

def createGIF():
    path='.'
    image_list=[]
    for filePath in (os.listdir(path)):
        if filePath.endswith('png') and filePath!='alpha.png':
            image_list.append(filePath)
    image_list.sort(key=sortKey)
    print(image_list)
    gif_name = 'created_gif.gif'
    create(image_list, gif_name)
