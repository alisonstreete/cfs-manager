import os
from cfs_manager import zipper

def main(dir_to_watch=os.getcwd()):
    location = os.path.split(os.path.abspath(zipper.__file__))[0]
    in_managed = False
    currdir = str(dir_to_watch)

    try:
        with open(os.path.join(location, 'managed.txt'), 'r') as managed:
            dirs = managed.read()
            if currdir in dirs:
                in_managed = True
    except FileNotFoundError:
        pass

    if not in_managed:
        with open(os.path.join(location, 'managed.txt'), 'a') as managed:
            line = '\n' + str(dir_to_watch)
            managed.write(line)

        with open('zipper.ignore', 'w') as ignore:
            ignore.write('zipper.ignore\n')
            ignore.write('cfs_watcher.py\n')

if __name__ == "__main__":
    main()
