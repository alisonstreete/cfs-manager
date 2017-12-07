from os import scandir
from cfs_manager import manager

def test_clean():
	"""Provides a clean filesystem to test and tests remove_all()"""
	fs = manager.Main_FS()
	fs.remove_all()
	files = fs.files
	assert files == []
	return fs

def test_upload():
	directory = "/home/alison/Dev/cfsm/test_uploads"
	fs = test_clean()
	fs.upload_archives(directory)
	cloud_files = set([file['filename'] for file in fs.files])
	local_files = set([str(file.name)+'.zip' for file in scandir(directory)])
	assert len(cloud_files) > 0
	assert cloud_files == local_files