import os, shutil
from file_systems import CloudFileSystem, GDrive_FS, PCloud_FS, DBox_FS
from file_systems import file_size_display

fs_classes = [['pCloud', PCloud_FS], ['Google Drive', GDrive_FS], ['Dropbox', DBox_FS]]

def start():
    fs_chosen = []  #Only have in the chosen list the FSs that were accepted during configuration
    with open('system_config.txt', 'r') as config:
        con = config.read()
        for cl in fs_classes:
            if cl[0] in con:
                fs_chosen.append(cl)
    fs_list = []
    for choice in fs_chosen:  #Initialise each filesystem in turn
        print("Initializing", choice[0] +"...")
        x = choice[1]()
        fs_list.append(x)
    return fs_list

def convert_gdrive(current_files):
    converted_files = []
    for f in current_files:
        new = {
            'system type' : 'Google Drive',
            'filename' : f['title'],
            'id' : f['id'],
            'date' : f['modifiedDate'],
            'original name' : f['originalFilename'],
            'size' : int(f['fileSize']),
            'trashed' : f['explicitlyTrashed'],
            'original file' : f
        }
        converted_files.append(new)
    return converted_files

def convert_pcloud(current_files):
    converted_files = []
    for f in current_files:
        new = {
            'system type' : 'pCloud',
            'filename' : f['name'],
            'id' : f['id'],
            'date' : f['modified'],
            'original name' : None,
            'size' : int(f['size']),
            'trashed' : False,
            'original file' : f
        }
        converted_files.append(new)
    return converted_files

def convert_dbox(current_files):
    converted_files = []
    for f in current_files:
        new = {
            'system type' : 'Dropbox',
            'filename' : f.name,
            'id' : f.id,
            'date' : f.client_modified,
            'original name' : None,
            'size' : int(f.size),
            'trashed' : False,
            'original file' : f
        }
        converted_files.append(new)
    return converted_files

def convert_files(fs):
    if fs.type == 'Google Drive':
        converted = convert_gdrive(fs.files)
    elif fs.type == 'pCloud':
        converted = convert_pcloud(fs.files)
    elif fs.type == 'Dropbox':
        converted = convert_dbox(fs.files)
    return converted

try:
    with open('managed.txt', 'r') as f:
        dirs = f.readlines()
        dirs = [x.strip() for x in dirs]        
        dirs = [x for x in dirs if x]
except FileNotFoundError:
    dirs = ''

def get_all_files(file_systems):
    all_files = []
    for sys in file_systems:
        all_files.extend(convert_files(sys))
    return all_files

def scantree(directory):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry

def get_folder_size(directory):
    size = 0
    for item in scantree(directory):
        if item.is_file():
            size += os.path.getsize(item.path)
    return size


class Main_FS(CloudFileSystem):
    def __init__(self):
        file_systems = start()
        files = get_all_files(file_systems)
        size = 0
        for f in files:
            size += f['size']
        total_quota = 0
        for fs in file_systems:
            total_quota += fs.get_quota()
        available_space = 0
        for fs in file_systems:
            available_space += fs.get_available()
        file_system_info = {
            'total quota' : total_quota,
            'available space' : available_space,
        }
        CloudFileSystem.__init__(self, 'main', file_systems, 0, size, files, file_system_info)

    def refresh_files(self):
        self.files = get_all_files(self.fs)
        self.cfs_size = 0
        for f in self.files:
            self.cfs_size += f['size']
        total_quota = 0
        for sys in self.fs:
            total_quota += sys.get_quota()
        available_space = 0
        for sys in self.fs:
            available_space += sys.get_available()
        self.file_system_info['total quota'] = total_quota
        self.file_system_info['available space'] = available_space

    def hard_refresh(self):
        for sys in self.fs:
            sys.refresh_files()
        self.refresh_files()

    def print_free_space(self, humanReadable=True, precision=2):
        if humanReadable:
            print("Your total free space is: ", file_size_display(self.file_system_info['available space'], precision))
        else:
            print("Your total free space is: ", self.file_system_info['available space'])

    def print_used_space(self, humanReadable=True, precision=2):
        if humanReadable:
            print("Your total space utilised by CFS_Manager is: ", file_size_display(self.cfs_size, precision))
        else:
            print("Your total space utilised by CFS_Manager is: ", self.cfs_size)

    def upload_archives(self, directory):
        for fs in self.fs:
            if fs.get_available() >= get_folder_size(directory):
                print("Uploading", directory)
                fs.upload_archives(directory)
                break
        else:
            print("Insufficient space in your cloud storage systems to upload this directory.")
            print("You may be able to upload this by breaking it into sub-directories.")
        self.refresh_files()

    def get_cloud(self, value, field='filename'):
        for file in self.files:
            if str(file[field]) == str(value):
                choice = file
                break
        else:
            print("No file with "+ field +" of "+ value)
            return
        for sys in self.fs:
            if choice['system type'] == sys.type:
                return sys

    def download_file(self, filename, destination_directory):
        return self.get_cloud(filename+'.zip').download_file(filename+'.zip', destination_directory)

    def inspect_file(self, filename):
        for f in self.files:
            if f['filename'] == filename+'.zip':
                file_dict = f
                break
        info = []
        for key in file_dict:
            statement = str(key) +" :  "+ str(file_dict[key])
            info.append(statement)
        return info

    def remove_file(self, filename):
        self.get_cloud(filename+'.zip').remove_file(filename+'.zip')
        self.refresh_files()

    def remove_all(self):
        for sys in self.fs:
            sys.remove_all()
        self.refresh_files()