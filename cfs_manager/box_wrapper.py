import sys, os, webbrowser
from boxsdk import OAuth2, Client, exception
from zipper import zip_all, extract

def split_tokens():
    """Derives authentication information from the redirect url"""
    print("Your browser was opened so authentication could take place.")
    url = input("Please paste the url you were redirected to after authorizing this app:  ")
    codes = url.split('?state=')[1]
    code_list = codes.split('&code=')
    csrf_received, auth_code = code_list[0], code_list[1]
    return csrf_received, auth_code

def store_token(content, save, access_token, refresh_token):
    """Updates the config file with the new authorization code"""
    new = save.split(':::')[0].strip() +' ::: '+ access_token +'<:>'+ refresh_token +'\n'
    lines = [new if x==save else x for x in content]
    with open('system_config.txt', 'w') as config:
        config.write(''.join(lines))

def get_tokens_from_file():
    with open('system_config.txt', 'r') as config:  #Acquires refresh_code from saved file
        content = config.readlines()
        for line in content:
            if 'Box (no drop)' in line:
                save = line
                break
        else:
            print("No token found on file")
            return [None, None], content, save
        tokens = save.split(':::')[1].strip()
        token_list = tokens.split('<:>')
        return token_list, content, save

def start():
    """Returns the client object that allows for filesystem access"""
    token_list, content, save = get_tokens_from_file()
    oauth = OAuth2(
        client_id='njpho6pdex32qwdp5bgvv2gchter0rdy',
        client_secret='YppmebR7prUxoHhjRogVIBcLSgBAw3sw',
        access_token= token_list[0],
        refresh_token= token_list[1],
    )
    
    try:
        access_token, refresh_token = oauth._refresh(token_list[0])
    except Exception:
        auth_url, csrf_token = oauth.get_authorization_url('http://localhost:2772')
        webbrowser.open(auth_url)
        csrf_received, auth_code = split_tokens()
        assert csrf_received == csrf_token
        access_token, refresh_token = oauth.authenticate(auth_code)

    store_token(content, save, access_token, refresh_token)
    return Client(oauth)

def get_root(client, recurse=True):
    """Gets the id of the CFS_Manager folder by scanning top dir for it.

    If one exists, it will be returned during the for loop.
    If not, it will be created, then the function will recurse once to get the new folder's ID.
    If one's not found the second time, it's assumed that a CFS_Manager folder cannot be created."""

    items = client.folder(folder_id='0').get_items(limit=100, offset=0)
    for item in items:
        if item.name == 'CFS_Manager':
            root_folder = item
            return root_folder
    else:
        client.folder(folder_id='0').create_subfolder('CFS_Manager')
        if recurse:
            return get_root(client, False)
        else:
            print('Error: Cannot create CFS_Manager folder')
            raise sys.exit(0)

def get_user(client):
    return client.user(user_id='me').get()

def get_all_files(client, root):
    return client.folder(folder_id=str(root.id)).get_items(limit=1024, offset=0)  #Will miss items if there are >2^10 files

def get_file(files, filename):
    for f in files:
        if f.name == filename:
            return f
    else:
        print('No file of that name found')

def upload_file(root, filepath):
    try:
        root.upload(filepath, os.path.split(filepath)[1])  #Crashes if file of the same name is in folder
    except exception.BoxAPIException:
        print("File of this name already exists.")

def upload_archives(root, currdir):
    files = zip_all(currdir)
    for f in files:
        upload_file(root, f.filename)

def download_file(files, filename):
    file = get_file(files, filename)
    file_binaries = file.content()

    os.makedirs(os.path.join(os.getcwd(), "file_swap"), exist_ok=True)
    destination = os.path.join("file_swap", filename)
    with open(destination, 'wb') as file_handle:
        file_handle.write(file_binaries)
    return extract(destination)

def delete_file(files, filename):
    get_file(files, filename).delete()

def delete_all(files):
    for f in files:
        f.delete()