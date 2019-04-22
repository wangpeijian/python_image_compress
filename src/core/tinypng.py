#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import os
import os.path
import sys
from optparse import OptionParser

import tinify
from PIL import Image

# 请替换为自己申请的Key
tinify.key = "mAZfPHstg7VeIEaTpfY1UNzMYU3YKMP8"
png_path = []
png_path_compressed = []


# 字节bytes转化kb\m\g
def limitSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    return kb < 1024 * 10


def get_png_path(inputPath):
    for p in os.listdir(inputPath):
        temp_path = os.path.join(inputPath, p)
        if os.path.isdir(temp_path):
            get_png_path(temp_path)
        else:
            if os.path.splitext(p)[1] == '.png' or os.path.splitext(p)[1] == 'jpg' or os.path.splitext(p)[1] == 'jpeg':
                print("PNG File:", os.path.join(inputPath, p))
                png_path.append(os.path.join(inputPath, p))


def compress_core(inputFile, outputFile, img_width):
    # 判断图片大小，过小的文件不需要压缩
    size = os.path.getsize(inputFile)
    if not limitSize(size):
        source = tinify.from_file(inputFile)
        if img_width is not None:
            resized = source.resize(method="scale", width=img_width)
            resized.to_file(outputFile)
        else:
            source.to_file(outputFile)


def compress_path(path, width):
    print("compress_path-------------------------------------")
    if not os.path.isdir(path):
        print("这不是一个文件夹，请输入文件夹的正确路径!")
        return
    else:
        fromFilePath = path  # 源路径
        toFilePath = path + "/tiny"  # 输出路径
        print("fromFilePath=%s" % fromFilePath)
        print("toFilePath=%s" % toFilePath)

        for root, dirs, files in os.walk(fromFilePath):
            print("root = %s" % root)
            print("dirs = %s" % dirs)
            print("files= %s" % files)
            for name in files:
                fileName, fileSuffix = os.path.splitext(name)
                if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
                    toFullPath = toFilePath + root[len(fromFilePath):]
                    toFullName = toFullPath + '/' + name
                    if os.path.isdir(toFullPath):
                        pass
                    else:
                        os.mkdir(toFullPath)
                    compress_core(root + '/' + name, toFullName, width)
            break  # 仅遍历当前目录


# 仅压缩指定文件
def compress_file(inputFile, width):
    print("compress_file-------------------------------------")
    if not os.path.isfile(inputFile):
        print("这不是一个文件，请输入文件的正确路径!")
        return
    print("file = %s" % inputFile)
    dirname = os.path.dirname(inputFile)
    basename = os.path.basename(inputFile)
    fileName, fileSuffix = os.path.splitext(basename)
    if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
        mkdir(dirname + "/tiny");
        png_path_compressed.append(dirname + "/tiny/" + basename)
        compress_core(inputFile, dirname + "/tiny/" + basename, width)
    else:
        print("不支持该文件类型!")


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")


def run(file, dir=None, width=None):
    if file is not None:
        print("仅压缩一个文件!")
        compress_file(file, width)  # 仅压缩一个文件
        pass
    elif dir is not None:
        print("压缩指定目录下的文件!")
        compress_path(dir, width)  # 压缩指定目录下的文件
        pass
    else:
        print("压缩当前目录下的文件!")
        compress_path(os.getcwd(), width)  # 压缩当前目录下的文件


def get_compressed_result():
    for png in png_path:
        run(os.path.abspath(png))
    rows = []
    row = ()
    for i in range(len(png_path)):
        img = Image.open(png_path[i])
        imgSize = img.size
        before_compressed = os.stat(png_path[i]).st_size
        after_compressed = os.stat(png_path_compressed[i]).st_size
        print(png_path[i], before_compressed, after_compressed,
              (before_compressed - after_compressed) * 1.0 / before_compressed)
        if imgSize[0] * imgSize[1] > 1024 * 1024:
            too_large_scale = "True"
        else:
            too_large_scale = "False"
        row = (png_path[i], before_compressed, after_compressed,
               (before_compressed - after_compressed) * 1.0 / before_compressed, imgSize[0], imgSize[1],
               too_large_scale)
        rows.append(row)
    header = [u'Path', u'before_compressed', u'after_compressed', u'compression_rate', u'width', u'height',
              u'too_large_scale']
    with open('compressed.csv', 'wb') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(rows)


if __name__ == "__main__":
    usage = '''python tinypng.py [options]
      -example: python tinypng.py -d xxx 
    '''
    parser = OptionParser(usage)
    parser.add_option('-d', dest='_path', help=u'(必选)指定游戏脚本路径')
    (options, args) = parser.parse_args()
    if not options._path:
        print('\n -d 参数必须设置！')
        print(usage)
        sys.exit(1)
    get_png_path(options._path)
    get_compressed_result()
