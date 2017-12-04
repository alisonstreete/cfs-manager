import os
from cfs_manager import zipper

def main():
    location = os.path.split(os.path.abspath(zipper.__file__))[0]
    in_managed = False
    currdir = str(os.getcwd())

    try:
        with open(os.path.join(location, 'managed.txt'), 'r') as managed:
            dirs = managed.read()
            if currdir in dirs:
                in_managed = True
    except FileNotFoundError:
        pass

    if not in_managed:
        with open(os.path.join(location, 'managed.txt'), 'a') as managed:
            line = '\n' + str(os.getcwd())
            managed.write(line)

        with open('zipper.ignore', 'w') as ignore:
            ignore.write('zipper.ignore\n')
            ignore.write('cfs_watcher.py\n')

if __name__ == "__main__":
    main()