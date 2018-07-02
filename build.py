import utils
import argparse as ArgParser
import tempfile
import os
import subprocess
import sys
import pip
from contextlib import redirect_stdout
import io

tmpLoc = tempfile.mkdtemp()
zippedLoc = tempfile.mkdtemp(suffix=".zip")
minPythonVersion = (3, 6)


def parseArgs():
	argParser = ArgParser.ArgumentParser(prog='ava', description='A utility script used to build the Ava tool.')
	argParser.add_argument('-i', '--integrate', action='store_true', help='integrate the tool with your system (requires root)')
	argParser.add_argument('-o', '--overwrite', action='store_true', help='write over already created files')
	argParser.add_argument('-f', '--file', metavar='FILE', help='the file export the built tool to')
	argParser.add_argument('-e', '--error', metavar='CODES', nargs='*', type=int, help="print the meaning behind the given error codes")
	return argParser.parse_args()


def exit(code):
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Cleaning up temporary directories and pycache")
	cleanUp(tmpLoc, zippedLoc, "__pycache__")

	if code == 0:
		utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Ava has been built successfully")
		sys.exit(0)
	if code == 1:
		utils.out(utils.LINE_H, "build: ", utils.WARN, "The build script exited due to user input with code 1")
		sys.exit(1)
	utils.out(utils.LINE_H, "build: ", utils.ERR, "The build script encountered a fatal error and exited with error code " + str(code))
	utils.out(utils.LINE_H, "build: ", utils.ERR, "Use the command ", utils.CMD, "python3 build.py -e " + str(code), utils.ERR, " to find out more")
	sys.exit(code)


def executeChecked(cmd, cmdName, stdout=None, stdin=None, out=True, cwd=None, errorCode=None, alterOut=None):
	if isinstance(cmd, tuple):
		errorCode = cmd[1]
		cmd = cmd[0]

	if not isinstance(cmd, str):
		utils.out(utils.LINE_H, "build: ", utils.PROG_ERR, "Cmd input is not a string in executeChecked (" + str(cmd) + ")")
		exit(-1)

	if errorCode == None:
		utils.out(utils.LINE_H, "build: ", utils.PROG_ERR, "Error code is None in executeChecked")
		exit(-1)

	popen = execute(cmd, stdout=stdout, stderr=subprocess.PIPE, stdin=stdin, out=out, cwd=cwd, shell=True, alterOut=alterOut)
	if not popen.returncode == 0:
		utils.out(utils.LINE_H, "build: ", utils.CMD, cmdName.capitalize(), utils.ERR, " finished with non-zero exit code (" + str(popen.returncode) + ") and message:")
		for line in popen.stderr:
			utils.out(utils.LINE_H, "build: " + cmdName + ": ", utils.ERR, line.decode("utf-8"), end="")
		exit(errorCode)
	return popen


def execute(cmd, stdout=None, stderr=None, stdin=None, shell=False, out=True, cwd=None, alterOut=None):
	if isinstance(cmd, list):
		readableCmd = " ".join(cmd)
	elif isinstance(cmd, str):
		readableCmd = cmd
	else:
		utils.out(utils.LINE_H, "build: ", utils.PROG_ERR, "Non list or string cmd (" + str(cmd) + ")")
		exit(-1)

	if shell:
		cmd = readableCmd
	if out:
		utils.out(utils.LINE_H, "build: ", utils.CMD, readableCmd, (alterOut if not alterOut == None else utils.CMD))
	popen = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell, cwd=cwd)
	popen.wait()
	return popen


def versionStr(tupledVersion):
	ver = str(tupledVersion[0]) + "." + str(tupledVersion[1])
	if len(tupledVersion) > 2:
		ver += "." + str(tupledVersion[2])
	if len(tupledVersion) > 3:
		ver += tupledVersion[3][0]
	if len(tupledVersion) > 4:
		ver += str(tupledVersion[4])
	return ver


def installDependencies():
	if sys.version_info < minPythonVersion:
		utils.out(utils.LINE_H, "build: ", utils.ERR, "It is required that you use Python " + versionStr(minPythonVersion) +
					" or higher to build and run Ava (built with version " + versionStr(sys.version_info) + ")")
		exit(12)

	f = io.StringIO()
	with redirect_stdout(f):
		pip.main(['install', '--user', 'configparser==3.5.0'])
	for line in f.getvalue().split("\n"):
		if not line == "":
			utils.out(utils.LINE_H, "build: pip: ", utils.OUT, line)

def build(args):
	if not args.file:
		utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Using default value 'ava' for output file")
		args.file = "ava"
	else:
		args.file = os.path.normpath(args.file)

	if args.integrate:
		utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Integrating Ava with your system")
		endLoc = os.path.join("/usr/local/bin/", os.path.basename(args.file))
		args.file = tempfile.mktemp()
		checkForOverwrite(endLoc, args.overwrite, sudo=True)

	checkForOverwrite(args.file, args.overwrite)

	execute(["rmdir", zippedLoc], out=False)

	gatherPythonFiles(tmpLoc)
	createMain(tmpLoc)
	zip(zippedLoc, tmpLoc)
	addShebang(zippedLoc, args.file)
	makeExecutable(args.file)
	if args.integrate:
		move(args.file, endLoc)


def checkForSudo():
	if os.getuid() == 0:
		utils.out(utils.LINE_H, "build: ", utils.WARN, "Running with root privileges will run pip with root privileges, which is not recommended and may result in inexpected behavior.")
		cont = utils.booleanQuery(utils.LINE_H, "build: ", utils.WARN, "Only continue if you only want to run ava with root.  Would you like to continue?", default=False)
		if cont:
			utils.out(utils.LINE_H, "build: ", utils.WARN, "Okay, but don't tell me I didn't warn you")
		else:
			exit(1)
#	if not os.getuid() == 0:
#		utils.out(utils.LINE_H, "build: ", utils.ERR, "Run with root privileges to integrate Ava with your system")
#		exit(2)


def checkForOverwrite(out, canOverwrite, sudo=False):
	if os.path.exists(out):
		if canOverwrite:
			write = utils.booleanQuery(utils.LINE_H, "build: ", utils.BWARN, "File '" + out + "' will be written over. Would you like to continue?", default=False)
			if write:
				utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Removing '" + out + "'")
				cleanUp(out, sudo=sudo)
			else:
				exit(1)
		else:
			utils.out(utils.LINE_H, "build: ", utils.ERR, "File '" + out + "' already exists")
			utils.out(utils.LINE_H, "build: ", utils.ERR, "    Try running with the ", utils.CMD, "--overwrite", utils.ERR, " or ", utils.CMD, "-o", utils.ERR, " flag to write over the existing file")
			exit(3)


def gatherPythonFiles(tmp):
	CP = ("cp *.py " + tmp, 5)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Gathering python files into the temporary directory")
	executeChecked(CP, "cp")


def createMain(tmp):
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Creating '__main__.py' file")
	try:
		with open(os.path.join(tmp, "__main__.py"), "w+") as file:
			file.write("import ava\nif __name == '__main__':\n\tava")
	except EnvironmentError as e:
		utils.out(utils.LINE_H, "build: ", utils.ERR, "Could not create/write to '__main__.py' file")
		utils.out(utils.LINE_H, "build: ", utils.ERR, "Full output:")
		for line in e.split("\n"):
			utils.out(utils.LINE_H, "build: \t", utils.ERR, line)
		exit(4)


def zip(zipLoc, tmp):
	ZIP = ("zip -r " + zipLoc + " *", 6)
#	MV_ZIP = ("mv " + zipLoc + " " + os.curdir, 7)

	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Zipping python files")
	executeChecked(ZIP, "zip", stdout=subprocess.PIPE, cwd=tmp)
#	executeChecked(MV_ZIP, "mv", cwd=tmp)


def addShebang(zip, out):
	version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
	ECHO = ("echo '#!/usr/bin/env python" + version + "'", 8)
	CAT = ("cat - " + zip + " > " + out, 9)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Adding shebang to the zip")
	echod = executeChecked(ECHO, "echo", stdout=subprocess.PIPE)
	executeChecked(CAT, "cat", stdin=echod.stdout)


def makeExecutable(out):
	CHMOD = ("chmod +x " + out, 10)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Making '" + out + "' executable")
	executeChecked(CHMOD, "chmod")


def move(file, loc):
	MV = ("sudo mv " + file + " " + os.path.normpath(loc), 2)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Moving '" + file + "' to '" + loc + "'")
	executeChecked(MV, "mv", alterOut=utils.BWARN)


def cleanUp(*tmps, out=True, sudo=False):
	for tmp in tmps:
		if os.path.exists(tmp):
			executeChecked(("sudo " if sudo else "") + "rm -rf " + tmp, "rm", out=out, errorCode=11, alterOut=(utils.BWARN if sudo else None))


def printErrors(codes):
	for code in codes:
		if code in errorMessages:
			utils.out(utils.LINE_H, "build: ", utils.ERR, "Error code " + str(code) + ": ", utils.STD_OUT, errorMessages[code])
		else:
			utils.out(utils.LINE_H, "build: ", utils.ERR, "Error code " + str(code) + " does not exist")


def main():
	utils.outputLevel = 0
	args = parseArgs()
	if not args.error:
		checkForSudo()
		installDependencies()
		build(args)
		exit(0)
	printErrors(args.error)


errorMessages = {
	-1: "This is a programming error, try submitting an issue at https://gitlab.com/tgrossb87/Ava/issues",
	0: "Ava has been built successfully",
	1: "User input terminated the program before the build process finished",
	2: "Could not move temporary file to /usr/local/bin",
#	2: "A non-root user attempted to use the integrate flag",
	3: "Attempted to write to already existing file without the overwrite flag",
	4: "An environment error occurred while editing '__main__.py', more info in the command's output",
	5: "Could not copy python files into temporary directory, more info in the command's output",
	6: "Could not create zipped file, more info in the command's output",
	7: "Could not move zipped file to parent directory, more info in the command's output",
	8: "Could not echo a line, more info in the command's output",
	9: "Could not cat to a file with echo input, more info in the command's output",
	10: "Could not make output file executable, more info in the command's output",
	11: "Could not remove file, more info in the command's output",
	12: "Python version out of date (< Python " + versionStr(minPythonVersion) + ")"
}

try:
	main()
except KeyboardInterrupt:
	exit(1)
