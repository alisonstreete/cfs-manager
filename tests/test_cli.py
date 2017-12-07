from os import scandir, path, remove
from cfs_manager.cli import find_text, evaluator
from cfs_manager.manager import Main_FS

def check_evaluation(fs, args_string):
	"""Base of CLI testing. Provide strings simulating console inputs, and check side effects."""
	cmd = find_text(args_string)
	print(cmd) #Remove
	if type(cmd) is list:
		cmd = cmd[0].split()+[cmd[1]]+cmd[2].split()
	else:
		cmd = cmd.split()
	evaluator(fs, cmd)

def test_upload():
	fs = Main_FS()
	fs.remove_all()
	check_evaluation(fs, ... )
	#insert directory to be uploaded from above
	files = fs.files
	assert len(files) > 0

def test_download():
	expected_file = 
	#Must use a string containing quotes around a filename
	download_directory = 
	#Must use a valid absolute path on testing machine
	
	check_evaluation(Main_FS(), "--download "+expected_file+" "+download_directory)
	download_names = [file.name for file in scandir(download_directory)]
	assert expected_file.strip("'") in download_names
	#When in downloads, there's be no quotes, so that must be stripped from the assertion
	remove(path.join(download_directory, expected_file.strip("'")))