import requests as req
from PIL import Image
from io import BytesIO
import os

def make_thumb(path, filename, sizes=(128, 128)):
    """
    生成指定尺寸缩略图
    :param path: 
    :param filename: 
    :param sizes: 指定尺寸
    :return: 无返回，直接保存图片
    """
    #response = req.get(url)
    #im = Image.open(BytesIO(response.content))
    im = Image.open(path + '/' + filename)
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    # 切成方图，避免变形
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            # h*h
            delta = (width - height) / 2
            box = (delta, 0, delta + height, height)
        else:
            # w*w
            delta = (height - width) / 2
            box = (0, delta, width, delta + width)
        region = im.crop(box)

    # resize
    thumb = region.resize((sizes[0], sizes[1]), Image.ANTIALIAS)
    #保存图片
    savename = path + '/tm/' + filename
    thumb.save(savename, quality=100)
	
path = os.getcwd()
print('当前目录：' + os.getcwd())
count = 0
subDirList = []
for dirName,subDir,files in os.walk(path):
		if count == 0:		#只扫描第一层目录
				subDirList = subDir
		count = count + 1
		
count = 0
for subdir in subDirList:
		print('【' + str(count) + '/' + str(len(subDirList)) + '】 目录:' + subDirList[count])
		tmdir = path + '/' + subDirList[count] + '/tm'
		isExists=os.path.exists(tmdir)
		if not isExists:
				os.makedirs(tmdir)	#创建缩略图目录
		filesList = os.listdir(subdir)
		for files in filesList:
				if(os.path.isfile(path + '/' + subDirList[count] + '/' + files)):
						ext = os.path.splitext(files)[-1]
						if(ext == '.jpg' or ext == '.jpeg' or ext == '.png' or ext == '.JPG' or ext == '.JPEG' or ext == '.PNG'):
								make_thumb(path + '/' + subDirList[count],files)
		count = count + 1