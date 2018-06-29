#!/usr/bin/env python3
import utils
import argparse as ArgParser
import tempfile
import os
import subprocess
import sys

tmpLoc = tempfile.mkdtemp(dir=".")
zippedLoc = tempfile.mkdtemp(suffix=".zip", dir=".")


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
	utils.out(utils.LINE_H, "build: ", utils.ERR, "The build script encountered a fatal error and exited with error code " + str(code))
	utils.out(utils.LINE_H, "build: ", utils.ERR, "Use the command ", utils.CMD, "./build.py -e " + str(code), utils.ERR, " to find out more")
	sys.exit(code)


def executeChecked(cmd, stdout=None, stdin=None, out=True, cwd=None, errorCode=None):
	if isinstance(cmd, tuple):
		errorCode = cmd[1]
		cmd = cmd[0]

	if not isinstance(cmd, str):
		utils.out(utils.LINE_H, "build: ", utils.PROG_ERR, "Cmd input is not a string in executeChecked (" + str(cmd) + ")")
		exit(-1)

	if errorCode == None:
		utils.out(utils.LINE_H, "build: ", utils.PROG_ERR, "Error code is None in executeChecked")
		exit(-1)

	popen = execute(cmd, stdout=stdout, stderr=subprocess.PIPE, stdin=stdin, out=out, cwd=cwd, shell=True)
	if not popen.returncode == 0:
		fs = cmd.index(" ")
		cmdName = cmd[:fs]
		cmd = cmd[:fs]
		if cmdName == "sudo":
			# Go to the next space
			cmdName = cmd[:cmd.index(" ")]
		utils.out(utils.LINE_H, "build: ", utils.CMD, cmdName.capitalize(), utils.ERR, " finished with non-zero exit code (" + str(popen.returncode) + ") and message:")
		for line in popen.stderr:
			utils.out(utils.LINE_H, "build: \t", utils.ERR, line.decode("utf-8"), end="")
		exit(errorCode)
	return popen


def execute(cmd, stdout=None, stderr=None, stdin=None, shell=False, out=True, cwd=None):
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
		utils.out(utils.LINE_H, "build: ", utils.CMD, readableCmd)
	popen = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell, cwd=cwd)
	popen.wait()
	return popen


def build(args):
	if not args.file:
		utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Using default value 'ava' for output file")
		args.file = "ava"
	if args.integrate:
		utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Integrating Ava with your system")
		args.file = os.path.join("/usr/local/bin", os.path.basename(args.file))
		checkForSudo()

	checkForOverwrite(args.file, args.overwrite)

	execute(["rmdir", zippedLoc], out=False)

	gatherPythonFiles(tmpLoc)
	createMain(tmpLoc)
	zip(zippedLoc, tmpLoc)
	addShebang(zippedLoc, args.file)
	makeExecutable(args.file)


def checkForSudo():
	if not os.getuid() == 0:
		utils.out(utils.LINE_H, "build: ", utils.ERR, "Run with root privileges to integrate Ava with your system")
		exit(2)


def checkForOverwrite(out, canOverwrite):
	if os.path.exists(out):
		if canOverwrite:
			write = utils.booleanQuery(utils.LINE_H, "build: ", utils.BWARN, "File '" + out + "' will be written over. Would you like to continue?", default=False)
			if write:
				utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Removing '" + out + "'")
				cleanUp(out)
			else:
				exit(1)
		else:
			utils.out(utils.LINE_H, "build: ", utils.ERR, "File '" + out + "' already exists")
			utils.out(utils.LINE_H, "build: ", utils.ERR, "    Try running with the ", utils.CMD, "--overwrite", utils.ERR, " or ", utils.CMD, "-o", utils.ERR, " flag to write over the existing file")
			exit(3)


def gatherPythonFiles(tmp):
	CP = ("cp *.py " + tmp, 5)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Gathering python files into the temporary directory")
	executeChecked(CP)


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
	MV_ZIP = ("mv " + zipLoc + " " + os.pardir, 7)

	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Zipping python files")
	executeChecked(ZIP, stdout=subprocess.PIPE, cwd=tmp)
	executeChecked(MV_ZIP, cwd=tmp)


def addShebang(zip, out):
	ECHO = ("echo '#!/usr/bin/env python3'", 8)
	CAT = ("cat - " + zip + " > " + out, 9)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Adding shebang to the zip")
	echod = executeChecked(ECHO, stdout=subprocess.PIPE)
	executeChecked(CAT, stdin=echod.stdout)


def makeExecutable(out):
	CHMOD = ("chmod +x " + out, 10)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Making '" + out + "' executable")
	executeChecked(CHMOD)


def cleanUp(*tmps, out=True):
	for tmp in tmps:
		if os.path.exists(tmp):
			executeChecked("rm -rf " + tmp, out=out, errorCode=11)


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
		build(args)
		exit(0)
	printErrors(args.error)


errorMessages = {
	-1: "This is a programming error, try submitting an issue at https://gitlab.com/tgrossb87/Ava/issues",
	0: "Ava has been built successfully",
	1: "User input terminated the program before the build process finished",
	2: "A non-root user attempted to use the integrate flag",
	3: "Attempted to write to already existing file without the overwrite flag",
	4: "An environment error occurred while editing '__main__.py', more info in the command's output",
	5: "Could not copy python files into temporary directory, more info in the command's output",
	6: "Could not create zipped file, more info in the command's output",
	7: "Could not move zipped file to parent directory, more info in the command's output",
	8: "Could not echo a line, more info in the command's output",
	9: "Could not cat to a file with echo input, more info in the command's output",
	10: "Could not make output file executable, more info in the command's output",
	11: "Could not remove file, more info in the command's output"
}
main()
