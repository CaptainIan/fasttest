
import argparse
from xffasttest.version import VERSION
from xffasttest.fasttest import FastTest

def custom_method(args) -> None:
    if args.run:
        fasttest = FastTest()
        fasttest.start()
    elif args.init:
        pass

def main() -> None:
    parser = argparse.ArgumentParser(description='fasttest 命令行工具')
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='')
    parser.add_argument('-r', '--run', action='store_true')
    parser.add_argument('-i', '--init', type=str)

    args = parser.parse_args()
    custom_method(args)

if __name__ == '__main__':
    main()