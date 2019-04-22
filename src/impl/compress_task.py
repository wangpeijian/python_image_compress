import os

import tinify

from config.system import TINY_PNG_API_KEY


def process(task, record):
    tinify.key = TINY_PNG_API_KEY

    input_root = task.source_path
    output_root = task.target_root_path

    for file in task.files:
        input_file = os.path.join(input_root, file)
        output_file = os.path.join(output_root, file)

        source = tinify.from_file(input_file)
        source.to_file(output_file)

        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)

        record['done'] = record['done'] + 1
        record['total_size'] = record['total_size'] + input_size
        record['result_size'] = record['result_size'] + output_size

        print(record['done'], "/", record['total'], "    ", input_file, "文件压缩率：", output_size / input_size)
