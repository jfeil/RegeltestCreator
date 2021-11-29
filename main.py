import sys
from bs4 import BeautifulSoup


def read_in(file_name):
    with open(file_name, 'r+') as file:
        soup = BeautifulSoup(file, "xml")
    print(soup)


if __name__ == '__main__':
    args = sys.argv
    read_in(args[1])
