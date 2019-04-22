import os

FILTER_CONDITION = ['.png', '.jpg', '.jpeg']


def limit_size(byte):
    byte = float(byte)
    kb = byte / 1024
    return kb < 10


def img_filter(root, files):
    filter_files = []
    total_size = 0

    for file in files:
        file_name, file_suffix = os.path.splitext(file)
        if file_suffix in FILTER_CONDITION:

            # 判断文件大小，小文件不处理
            size = os.path.getsize(os.path.join(root, file))
            if not limit_size(size):
                filter_files.append(file)
                total_size += size

    return filter_files
