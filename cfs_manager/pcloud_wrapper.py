import os
from pcloud import api
from zipper import zip_all, extract

folder_dict = {
    'path' : '/CFS_Manager'
    }

def start():
    """Initializes the PyCloud object that acts as a filesystem abstraction"""
    with open('system_config.txt', 'r') as config:  #Acquires email from saved file
        content = config.readlines()
        for line in content:
            if 'pCloud' in line:
                save = line
                break
        user = save.split(':::')[1].strip()
    pswd = input("pCloud Password: ")
    fs = api.PyCloud(user, pswd)
    folder = fs.listfolder(**folder_dict)
    if 'error' in folder:
        folder = fs.createfolder(**{'folderid' : '0', **folder_dict})
    return fs

def get_folder_id(fs):
    folder = fs.listfolder(**folder_dict)
    return folder['metadata']['folderid']

def get_files(fs, folder_id):
    return fs.listfolder(**{'folderid' : folder_id})['metadata']['contents']

def get_a_file(all_files, field, value):
    for file in all_files:
        if file[field] == value:
            return file
    else:
        print("No file with "+ field +" of "+ value)

def get_all_files(fs, folder_id=None):
    if not folder_id:
        folder_id = get_folder_id(fs)

    response = get_files(fs, folder_id)
    resp = []
    for r in response:
        if r['isfolder']:
            new = get_files(fs, r['folderid'])
            try:
                resp += new
            except:
                pass
    resp += [r for r in response if not r['isfolder']]
    return resp

def get_used_space(fs, folder_id=None):
    files = get_all_files(fs, folder_id)
    total_size = 0
    for f in files:
        total_size += int(f['size'])
    return total_size

def download_file(fs, filename):
    """Downloads a file (including zipped directories) from pCloud into cfs-m's swap folder"""
    file_path = folder_dict['path'] + '/' + filename
    file_descriptor = fs.file_open(**{'flags' : '0', 'path' : file_path})
    file_descriptor['count'] = str(2**40)  #Says to download upto a TB worth of the file, which will hopefully never be too low a limit.
    file_binaries = fs.file_read(**file_descriptor)

    os.makedirs(os.path.join(os.getcwd(), "file_swap"), exist_ok=True)
    destination = os.path.join("file_swap", filename)
    with open(destination, 'wb') as file_handle:
        file_handle.write(file_binaries)
    return extract(destination)

def remove_file(fs, filename):
    file_path = folder_dict['path'] + '/' + filename
    fs.deletefile(**{'path' : file_path})

def remove_all(fs):
    files = get_all_files(fs)
    for f in files:
        remove_file(fs, f['name'])

def upload_file(fs, file_path):
    fs.uploadfile(**{'files' : [file_path], 'folderid' : get_folder_id(fs)})

def upload_archives(fs, currdir):
    files = zip_all(currdir)
    for f in files:  #Done iteratively because uploadfile() only successfully uploads a single element in a list.
        fs.uploadfile(**{'files' : [f.filename], 'folderid' : get_folder_id(fs)})

def inspect(fs, file):
    info = []
    for key in file:
        statement = str(key) +" :  "+ str(file[key])
        if type(file[key]) == dict:
            statement += "  (dict)"
        info.append(statement)
    return info