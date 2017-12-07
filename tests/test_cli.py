from os import scandir, path, remove
from cli import find_text, evaluator
from manager import Main_FS

def check_evaluation(fs, args_string):
	"""Base of CLI testing. Provide strings simulating console inputs, and check side effects."""
	cmd = find_text(args_string)
	if type(cmd) is list:
		cmd = cmd[0].split()+[cmd[1]]+cmd[2].split()
		print(cmd)
	else:
		cmd = cmd.split()
	evaluator(fs, cmd)

def test_upload():
	fs = Main_FS()
	fs.remove_all()
	check_evaluation(fs, "--upload /home/alison/Dev/cfsm/test_uploads/muş")
	files = fs.files
	assert len(files) > 0

def test_download():
	expected_file = "'Beyoncé - Countdown.mp3'"
	#Must use a string containing quotes around a filename
	download_directory = '/home/alison/Downloads'
	#Must use a valid absolute path on testing machine
	fs = Main_FS

	evaluee = "--download "+expected_file+" "+download_directory
	check_evaluation(fs, evaluee)
	download_names = [file.name for file in scandir(download_directory)]
	for name in download_names:
		print(name)
	assert expected_file.strip("'") in download_names
	#When in downloads, there's be no quotes, so that must be stripped from the assertion
	remove(path.join(download_directory, expected_file.strip("'")))