import os, shutil
from file_systems import CloudFileSystem, PCloud_FS, GDrive_FS, DBox_FS, _Box_FS

fs_classes = [['pCloud', PCloud_FS], ['Google Drive', GDrive_FS], ['Dropbox', DBox_FS], ['Box (no drop)', _Box_FS]]

def start():
    """Initializes all selected file system classes and returns list of objects to Main_FS object"""
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
    """Converts the information in GDrive file metadata to a standardized format"""
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

def convert_box(current_files):
    converted_files = []
    for f in current_files:
        new = {
            'system type' : 'Box',
            'filename' : f.name,
            'id' : f.id,
            'date' : None,  #information not returned via Box SDK (wtf)
            'original name' : None,
            'size' : 0,  #information not returned via Box SDK (wtf)
            'trashed' : False,
            'notes' : 'File size displayed is inaccurate due to problems using the Box API',
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
    elif fs.type == 'Box':
        converted = convert_box(fs.files)
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
            yield from scantree(entry.path)
        else:
            yield entry

def get_folder_size(directory):
    size = 0
    for item in scantree(directory):
        if item.is_file():
            size += os.path.getsize(item.path)
    return size

def file_size_display(size, precision):
    """Displays human-readable file information, to [precision] decimal places"""
    suffixes=['B','KiB','MiB','GiB','TiB', 'PiB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 5:
        suffixIndex += 1
        size = size/1024.0
    return "%.*f%s"%(precision, size, suffixes[suffixIndex])


class Main_FS(CloudFileSystem):
    """The top-level file system abstraction which utilizes all other FSs"""
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
        """Forces all lower-level filesystems to refresh their file lists

        As opposed to refreshing files from info already stored in the other file systems, as is default"""
        for sys in self.fs:
            sys.refresh_files()
        self.refresh_files()

    def print_free_space(self, humanReadable=True, precision=2):
        if humanReadable:
            print("Your total free space is: ", file_size_display(self.file_system_info['available space'], precision))
        else:
            print("Your total free space is: ", self.file_system_info['available space'])

    def print_used_space(self, humanReadable=True, precision=2):
        if any(x.type == "Box" for x in self.fs):
            note = '\nNB: Box does not return file size info, so the files stored there are not counted.'
        else:
            note = ''

        if humanReadable:
            print("Your total space utilised by CFS_Manager is: ", file_size_display(self.cfs_size, precision), note)
        else:
            print("Your total space utilised by CFS_Manager is: ", self.cfs_size, note)

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

    def name_complete(self, filebeginning):
        """Autocompletes a partial filename using the list of known files"""
        for f in self.files:
            if f['filename'].startswith(filebeginning):
                print("(Completed as '"+ f['filename'].replace('.zip', '') +"')")
                return f['filename'].replace('.zip', '')

    def get_cloud(self, value, field='filename'):
        """Determines which cloud a given file was uploaded to"""
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