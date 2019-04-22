from optparse import OptionParser

from impl.scan_path import scan


def compress_path():
    print("开始运行")
    usage = '''python src [options]
      -example: python src -d xxx 
    '''
    parser = OptionParser(usage)
    parser.add_option('-d', dest='root_path')
    options, args = parser.parse_args()

    if not options.root_path:
        print('\n -d 参数必须设置！')
        print(usage)
        return

    scan(options.root_path)
