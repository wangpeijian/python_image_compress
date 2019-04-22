import os
import os.path

from entity.task_entity import Task
from impl.compress_task import process
from impl.convert import byte2m
from impl.file_filter import img_filter
from impl.folder import get_target_path, rmrf


def scan(root_path):
    print("开始扫描路径：", root_path)

    target_path = get_target_path(root_path)
    rmrf(target_path)

    task_list = []

    file_len = 0
    for root, dirs, files in os.walk(root_path):

        # 过滤图片文件
        files = img_filter(root, files)

        file_len += len(files)

        if file_len != 0:
            path_task = Task(root, root.replace(root_path, target_path), files)
            task_list.append(path_task)

    print("扫描到的文件数：", file_len)

    record = {'total': file_len, 'done': 0, 'total_size': 0, 'result_size': 0}
    for task in task_list:
        process(task, record)

    total_size = record['total_size']
    result_size = record['result_size']
    reduce_size = total_size - result_size

    print("文件输出目录:", target_path)
    print("压缩文件数:", file_len)
    print("压缩前大小： %s m" % byte2m(total_size))
    print("压缩后大小： %s m" % byte2m(result_size))
    print("整体压缩率： %s m" % (result_size / total_size))
    print("减小体积共： %s m" % byte2m(reduce_size))
