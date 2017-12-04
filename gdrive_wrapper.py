import os
from pydrive.auth import GoogleAuth, AuthenticationError
from pydrive.drive import GoogleDrive
from pydrive.drive import GoogleDriveFile as GDFile
from zipper import zip_all, extract

def start():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("gdrive_credentials.txt")
    # Try to load saved client credentials
    try:
        gauth.Authorize()
    except AuthenticationError:
        gauth.LocalWebserverAuth()
        # If there are no valid credentials to load, use the web validation flow
    gauth.SaveCredentialsFile("gdrive_credentials.txt")

    return GoogleDrive(gauth)

def get_drive_data(drive):
    return drive.GetAbout()

def get_folder_id(drive):
    folder_id = None
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for f in file_list:
        if f['title'] == 'CFS_Manager':
            folder_id = f['id']
            return folder_id
    else:
        folder = drive.CreateFile({'title': 'Cloud Manager',
        "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        return folder['id']

def get_all_files(folder, drive):
    query = {'q': "'{}' in parents and trashed=false".format(folder)}
    return drive.ListFile(query).GetList() #Returns a list of dictionaries

def get_file(all_files, field, value):
    for file in all_files:
        if file[field] == value:
            return file
    else:
        print("No file with "+ field +" of "+ value)

def upload_archives(currdir, folder_id, drive):
    files = zip_all(currdir)
    for f in files:
        new = GDFile()
        new.SetContentFile(f.filename)
        new_name = os.path.split(f.filename)[1]
        new['title'] = new_name
        new['parents'] = [{'id': folder_id}]
        new.Upload()

def remove_file(file):
    try:
        file.Trash()
    except AttributeError:  #There's no file to Trash, so .Trash() is undefined
        print("No file", file, "exists")

def download_file(file, filename):
    #file is a GDFile object, not an id
    os.makedirs(os.path.join(os.getcwd(), "file_swap"), exist_ok=True)
    destination = os.path.join("file_swap", filename)
    try:
        file.GetContentFile(destination)
        return extract(destination)
    except AttributeError:  #If the file being downloaded doesn't exist
        pass

def inspect(file):
    info = []
    for key in file:
        statement = str(key) +" :  "+ str(file[key])
        if type(file[key]) == dict:
            statement += "  (dict)"
        info.append(statement)
    return info