import sys, os, pathlib, shutil
from datetime import datetime
from zipfile import ZipFile

homedir = str(os.getcwd())

def zip_file(file, currdir):
    os.makedirs(os.path.join(homedir, "archives"), exist_ok=True)
    with ZipFile((os.path.join("archives", file) + '.zip'), 'a') as newzip:
        newzip.write(os.path.join(currdir, file), file)
        #1st arg zips the file at the named location; 2nd arg ensures name in archive isn't the full path
        return newzip

def zip_directory(directory, currdir):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(currdir+directory):  #Finds all files in the checked directory
        for x in filenames:
            localdir = dirpath.replace((currdir+directory), "")  #Takes directory tree below the src folder
            new = localdir +"/"+ x  #Concats the directory and file name, making it unique within the src folder
            new = new[1:]  #Drops the leading slash
            new = '/'.join(new.split('\\'))  #Changes to POSIX file path, if on Windows, to ensure compatibility with the zipinfo filename
            files.append(new)

    archived = []
    try:
        with ZipFile((directory[1:] + ".zip"), 'r') as myzip:
            for item in myzip.infolist():
                if item.filename[-1] != "/":
                    archived.append(item.filename)
                    #Does not append directory names (which end in '/')
    except FileNotFoundError:
        pass

    os.makedirs(os.path.join(homedir, "archives"), exist_ok=True)
    shutil.make_archive((os.path.join("archives", directory[1:])), 'zip', (os.path.join(currdir, directory[1:])))
    #This remakes the directory from scratch each time. Find way around that.

    with ZipFile(os.path.join("archives", (directory[1:] + '.zip')), 'a') as newzip:
        return newzip

def zip_all(currdir):
    files = [f for f in os.listdir(currdir) if os.path.isfile(os.path.join(currdir, f))]
    dirs = ["\\"+d for d in os.listdir(currdir) if os.path.isdir(os.path.join(currdir, d))]
    
    try:  #Try to open a zipper.ignore file to determine which files not to zip
        with open(os.path.join(currdir, 'zipper.ignore'), 'r') as ignore:
            items = ignore.readlines()  #Read each line as a file or directory to ignore
            items = [x.strip() for x in items]
            for x in items:
                try:
                    files.remove(x)
                except ValueError:
                    pass
                try:
                    dirs.remove(x)
                except ValueError:
                    pass
    except (FileNotFoundError, ValueError): #If there's no zipper.ignore file, zip everything
        pass

    all_zips = []
    for f in files:
        all_zips.append(zip_file(f, currdir))
    for d in dirs:
        all_zips.append(zip_directory(d, currdir))
    return all_zips

def extract(file_location):
    if '.' in file_location.replace('.zip', ''):  #if the non-zip filename has a dot (i.e, if it's not a folder), then...
        new_location = os.path.split(file_location)[0]  #just copy to the directory
    else:
        new_location = file_location.replace('.zip', '')  #copy into a folder with the same name as the zip (but no suffix)
    with ZipFile(file_location, 'r') as file:
        file.extractall(new_location)
        file_path = file.filename
        abs_file_path = os.path.join(homedir, file_path)
    os.remove(file_path)
    return abs_file_path.replace('.zip', '')