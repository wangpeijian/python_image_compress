import os
import shutil


def get_target_path(root_path):
    return root_path + "_compress"


def rmrf(target_path):
    if os.path.exists(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                os.remove(os.path.join(root, file))
        shutil.rmtree(target_path)
    print("清空目录：", target_path)


def mdir(path):
    os.makedirs(path)
    print("创建目录：", path)
