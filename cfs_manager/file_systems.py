from datetime import datetime
import os, shutil
import gdrive_wrapper as gdrive
import pcloud_wrapper as pcloud
import dropbox_wrapper as dbox
import box_wrapper as _box

try:
    with open('managed.txt', 'r') as f:
        dirs = f.readlines()
        dirs = [x.strip() for x in dirs]        
        dirs = [x for x in dirs if x]
except FileNotFoundError:
    dirs = ''

def download_move(filename, abs_file_path, new_file_location):
    if '.' in new_file_location:  #If it has a file extension
        shutil.copyfile(abs_file_path, new_file_location)
    else:  #If it's a folder
        shutil.copytree(abs_file_path, new_file_location)
    print("'"+filename.replace('.zip', '')+"'", "was downloaded.")

def download_cleanup(decorated):
    """Cleans up after downloads by putting them in the right directory and removing unneeded files/directories

    Wraps the download processes of individual file systems.
    Copies newly extracted files from place where the zip is downloaded.
    Deletes this download location as cleanup."""
    def wrapper(self, filename, destination_directory):
        abs_file_path, new_file_location = decorated(self, filename, destination_directory)
        download_move(filename, abs_file_path, new_file_location)
        shutil.rmtree(os.path.split(abs_file_path)[0])  #Removes the swap directory where the file was extracted
        return new_file_location
    return wrapper


class CloudFileSystem:
    """The framework within which all defined filesystems fall, to ensure a consistent API

    This class should never be instantiated directly.
    Other classes should simply inherit from it to ensure identical attributes.
    Contributers should use this as the template for any new cloud FSs added.
    This solves the problem of all the SDKs used having radically different calls and returns."""

    def __init__(self, fs_name, filesystem, root_id, cfs_size, files, file_system_info):
        self.type = fs_name
        #The standard, human-readable name for the file system
        self.fs = filesystem
        #An object representing the filesystem and connecting via the API
        self.root_id = root_id
        #The id of CFS_Manager's root folder in a given cloud
        self.cfs_size = cfs_size 
        #The total size of all files stored in a cloud (in bytes)
        self.files = files
        #A list of all files, in their default dictionary or object form, according to the SDK used
        #Will need to be passed back and forth between the manager and that cloud's wrapper
        self.file_system_info = file_system_info
        #A dictionary of information about the entire user account, if the API returns account info
        #It need not be the wrapper's standard format, as it's only used at a higher level

    def refresh_files(self):
        """Query the API for updated information on all files and account info

        To be used after any operation that might alter the files or attributes of an account.
        Should update the data stored in the class instance with the results of these queries."""
        pass

    def get_quota(self):
        """Returns the total space allocated to the user for this account"""
        pass

    def get_available(self):
        """Returns the total storage space available for new data"""
        pass

    def upload_archives(self, directory):
        """Uploads all files and folders from the named directory to the relevant cloud"""
        pass

    def upload_all(self):
        """Uploads all the files/folders in every directory listed in managed.txt"""
        for d in dirs:
            self.upload_archives(d)

    def download_file(self, filename, destination_directory):
        """Given a certain file name, download that file to the destination directory"""
        pass

    def inspect_file(self, filename):
        """Returns the attributes of the named file as a dictionary"""
        pass

    def remove_file(self, filename):
        """Deletes/trashes the named file in cloud storage

        Trashing a file is preferrable to deleting it for any cloud storage provider that allows the option.
        This method should NEVER affect the files in local storage."""
        pass

    def remove_all(self):
        """Iteratively performs file-removal on all files in the file system"""
        pass

class _Box_FS(CloudFileSystem):
    def __init__(self):
        fs = _box.start()
        root_id = _box.get_root(fs)  #object representing the 'CFS_Manager' folder itself; not just id
        cfs_size = None  #_Box doesn't let you check the size of a file (the attribute described in the docs doesn't exist)
        files = _box.get_all_files(fs, root_id)
        file_system_info = _box.get_user(fs)

        CloudFileSystem.__init__(self, 'Box', fs, root_id, cfs_size, files, file_system_info)

    def refresh_files(self):
        self.files = _box.get_all_files(self.fs, self.root_id)
        self.file_system_info = _box.get_user(self.fs)

    def get_quota(self):
        return self.file_system_info.space_amount

    def get_available(self):
        return int(self.file_system_info.space_amount) - int(self.file_system_info.space_used)

    def upload_archives(self, directory):
        _box.upload_archives(self.root_id, directory)
        self.refresh_files()

    @download_cleanup
    def download_file(self, filename, destination_directory):
        abs_file_path = _box.download_file(self.files, filename)
        new_file_location = os.path.join(destination_directory, filename.replace('.zip', ''))
        return abs_file_path, new_file_location

    def inspect_file(self, filename):
        pass

    def remove_file(self, filename):
        _box.delete_file(self.files, filename)
        self.refresh_files()

    def remove_all(self):
        _box.delete_all(self.files)
        self.refresh_files()

class DBox_FS(CloudFileSystem):
    def __init__(self):
        fs = dbox.start()
        root_id = ''
        #The Dropbox app is setup to treat the 'CFS_Manager' folder as root
        files = dbox.get_all_files(fs)
        cfs_size = dbox.get_used_space(files)
        file_system_info = dbox.get_user_info(fs)

        CloudFileSystem.__init__(self, 'Dropbox', fs, root_id, cfs_size, files, file_system_info)

    def refresh_files(self):
        self.files = dbox.get_all_files(self.fs)
        self.cfs_size = dbox.get_used_space(self.files)
        self.file_system_info = dbox.get_user_info(self.fs)

    def get_quota(self):
        return self.file_system_info['totalSpace']

    def get_available(self):
        return int(self.file_system_info['totalSpace']) - int(self.file_system_info['spaceUsed'])

    def upload_archives(self, directory):
        dbox.upload_archives(self.fs, directory)
        self.refresh_files()

    @download_cleanup
    def download_file(self, filename, destination_directory):
        abs_file_path = dbox.download_file(self.fs, filename)
        new_file_location = os.path.join(destination_directory, filename.replace('.zip', ''))
        return abs_file_path, new_file_location

    def inspect_file(self, filename):
        info = dbox.get_a_files_info(self.files, 'title', filename)
        statements = []
        for data in info:
            statements.append(data +" : "+ str(info[data]))
        return statements

    def remove_file(self, filename):
        dbox.delete_file(self.fs, filename)
        self.refresh_files()

    def remove_all(self):
        for f in self.files:
            dbox.delete_file(self.fs, f.name)
        self.refresh_files()

class PCloud_FS(CloudFileSystem):
    def __init__(self):
        fs = pcloud.start()
        root_id = pcloud.get_folder_id(fs)
        cfs_size = pcloud.get_used_space(fs)
        self.account_usage = pcloud.get_used_space(fs, '0')
        #As pCloud doesn't return user account data, no filesystem info is provided here
        #As a substitute, the total account usage level is calculated by counting all files
        #The inspection proceeds from 0 to ensure it's counting everything under the *account* root
        files = pcloud.get_all_files(fs)

        CloudFileSystem.__init__(self, 'pCloud', fs, root_id, cfs_size, files, {})

    def refresh_files(self):
        self.files = pcloud.get_all_files(self.fs)
        self.cfs_size = pcloud.get_used_space(self.fs)
        self.account_usage = pcloud.get_used_space(self.fs, '0')

    def get_quota(self):
        return 10*(2**30)
        #The API provides no way to view available space, so the min for free accounts is assumed

    def get_available(self):
        return 10*(2**30) - int(self.account_usage)

    def upload_archives(self, directory):
        pcloud.upload_archives(self.fs, directory)
        self.refresh_files()

    @download_cleanup
    def download_file(self, filename, destination_directory):
        abs_file_path = pcloud.download_file(self.fs, filename)
        new_file_location = os.path.join(destination_directory, filename.replace('.zip', ''))
        return abs_file_path, new_file_location

    def inspect_file(self, filename):
        file = pcloud.get_a_file(self.files, 'name', filename)
        info = pcloud.inspect(self.fs, file)
        return info

    def remove_file(self, filename):
        pcloud.remove_file(self.fs, filename)
        self.refresh_files()

    def remove_all(self):
        pcloud.remove_all(self.fs)
        self.refresh_files()

class GDrive_FS(CloudFileSystem):
    def __init__(self):
        fs = gdrive.start()
        root_id = gdrive.get_folder_id(fs)
        files = gdrive.get_all_files(root_id, fs)
        cfs_size = 0
        for f in files:
            cfs_size += int(f['fileSize'])
        file_system_info = gdrive.get_drive_data(fs)

        CloudFileSystem.__init__(self, 'Google Drive', fs, root_id, cfs_size, files, file_system_info)

    def refresh_files(self):
        self.files = gdrive.get_all_files(self.root_id, self.fs)
        self.cfs_size = 0
        for f in self.files:
            self.cfs_size += int(f['fileSize'])
        file_system_info = gdrive.get_drive_data(self.fs)

    def get_quota(self):
        return int(self.file_system_info['quotaBytesTotal'])

    def get_available(self):
        return int(self.file_system_info['quotaBytesTotal']) - int(self.file_system_info['quotaBytesUsedAggregate'])

    def upload_archives(self, directory):
        gdrive.upload_archives(directory, self.root_id, self.fs)
        self.refresh_files()

    @download_cleanup
    def download_file(self, filename, destination_directory):
        abs_file_path = gdrive.download_file(gdrive.get_file(self.files, 'title', filename), filename)
        new_file_location = os.path.join(destination_directory, filename.replace('.zip', ''))
        return abs_file_path, new_file_location

    def inspect_file(self, filename):
        file = gdrive.get_file(self.files, 'title', filename)
        info = gdrive.inspect(file)
        return info

    def remove_file(self, filename):
        gdrive.remove_file(gdrive.get_file(self.files, 'title', filename))
        self.refresh_files()

    def remove_all(self):        
        for f in self.files:
            self.remove_file(f['title'])
        self.refresh_files()