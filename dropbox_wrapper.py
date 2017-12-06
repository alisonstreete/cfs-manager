import os, platform, datetime, webbrowser
from dropbox import Dropbox
from dropbox.files import WriteMode
from dropbox import DropboxOAuth2FlowNoRedirect
from zipper import zip_all, extract

CHUNK_SIZE = 2**25  #i.e, 32MiB

def update_config(content, save, auth_code):
    """Updates the config file with the new authorization code"""
    new = save.split(':::')[0] + ' ::: ' + auth_code + '\n'
    lines = [new if x==save else x for x in content]
    with open('system_config.txt', 'w') as config:
        config.write(''.join(lines))

def start():
    """Initializes the Dropbox object that acts as a filesystem abstraction"""
    with open('system_config.txt', 'r') as config:  #Acquires auth_code from saved file
        content = config.readlines()
        for line in content:
            if 'Dropbox' in line:
                save = line
                break
        auth_code = save.split(':::')[1].strip()
    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception:
        auth_flow = DropboxOAuth2FlowNoRedirect('dd3vt2v1p0tey6b', '27183ha8su8lggd')
        authorize_url = auth_flow.start()
        webbrowser.open(authorize_url)
        auth_code = input("Enter the authorization code here: ").strip()
        update_config(content, save, auth_code)
        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception:
            pass
    return Dropbox(oauth_result.access_token)

def get_user_info(dbx):
    """Acquires the user's account info and converts to a dictionary"""
    client = dbx.users_get_current_account()
    space = dbx.users_get_space_usage()

    metadata_dict = {
    'username' : client.name.display_name,
    'id' : client.account_id,
    'email' : client.email,
    'spaceUsed' : space.used,
    'totalSpace' : space.allocation.get_individual().allocated
    }
    return metadata_dict

def get_all_files(dbx):
    return dbx.files_list_folder('').entries

def inspect_file(file):
    dict_file = {
        "title" : file.name,
        "id" : file.id,
        "modifiedDate" : file.client_modified,
        "size" : file.size,
        }
    return dict_file

def get_a_files_info(all_files, field, value):
    for f in all_files:
        info = inspect_file(f)
        if info[field] == value:
            return info
    else:
        print("No file with "+ field +" of "+ value)

def upload_file(dbx, LOCALFILE):
    """Uploads a local file to Dropbox in chunks <=4MiB each"""
    with open(LOCALFILE, 'rb') as f:
        BACKUPPATH = '/' + os.path.split(LOCALFILE)[1]
        file_size = os.path.getsize(LOCALFILE)
        if file_size <= CHUNK_SIZE:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        else:
            upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
            cursor = dbx.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=f.tell())
            commit = dbx.files.CommitInfo(path=BACKUPPATH)
            while f.tell() < file_size:
                if ((file_size - f.tell()) <= CHUNK_SIZE):
                    dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                else:
                    dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                    cursor.offset = f.tell()

def upload_archives(dbx, currdir):
    files = zip_all(currdir)
    for f in files:
        upload_file(dbx, f.filename)

def download_file(dbx, filename):
    """Downloads a file (including zipped directories) from Dropbox into cfs-m's swap folder"""
    metadata, response = dbx.files_download("/"+filename)
    file_binaries = response.content

    os.makedirs(os.path.join(os.getcwd(), "file_swap"), exist_ok=True)
    destination = os.path.join("file_swap", filename)
    with open(destination, 'wb') as file_handle:
        file_handle.write(file_binaries)
    return extract(destination)

def delete_file(dbx, filename):
    dbx.files_delete("/"+filename)

def list_files(files):
    file_list = []
    for f in files:
        file_list.append(inspect_file(f)['filename'])  #Inspects a file and returns a dict, then takes the 'filename' from dict, then appends to file_list
    return file_list

def get_used_space(files):
    used_space = 0
    for f in files:
        used_space += inspect_file(f)['size']
    return used_space