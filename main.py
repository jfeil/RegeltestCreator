import sys


def read_in(file_name):
    print(f"reading in {file_name}")


if __name__ == '__main__':
    args = sys.argv
    read_in(args[1])
