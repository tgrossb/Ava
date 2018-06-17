#!/usr/bin/env python3
import utils
import argparse as ArgParser
import tempfile
import os
import subprocess


def parseArgs():
	argParser = ArgParser.ArgumentParser(prog='ava', description='A utility script used to build the Ava tool.')
	argParser.add_argument('-i', '--integrate', action='store_true', help='integrate the tool with your system (requires root)')
	argParser.add_argument('-o', '--overwrite', action='store_true', help='write over already created files')
	argParser.add_argument('-f', '--file', help='the file export the built tool to')
	return argParser.parse_args()


def executeChecked(cmd, stdout=None, stdin=None, shell=False, out=True, cwd=None):
	popen = execute(cmd, stdout=stdout, stderr=subprocess.PIPE, stdin=stdin, shell=shell, out=out, cwd=cwd)
	if not popen.returncode == 0:
		cmdName = cmd[0]
		if cmd[0] == "sudo":
			cmdName = cmd[1]
		utils.out(utils.LINE_H, "build: ", utils.CMD, cmdName.capitalize(), utils.ERR, " finished with non-zero exit code (" + str(popen.returncode) + ") and message:")
		for line in popen.stderr:
			utils.out(utils.LINE_H, "build: \t", utils.ERR, line.decode("utf-8"), end="")
		utils.exit(silent=True)
	return popen


def execute(cmd, stdout=None, stderr=None, stdin=None, shell=False, out=True, cwd=None):
	readableCmd = " ".join(cmd)
	if shell:
		cmd = readableCmd
	if out:
		utils.out(utils.LINE_H, "build: ", utils.CMD, readableCmd)
	popen = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell, cwd=cwd)
	popen.wait()
	return popen


def build():
	args = parseArgs()
	utils.outputLevel = 0
	if not args.file:
		utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Using default value 'ava' for output file")
		args.file = "ava"
	if args.integrate:
		utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Integrating Ava with your system")
		if not args.file == "ava":
			utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Ignoring file argument for integration")
		args.file = "/usr/local/bin/ava"
		checkForSudo()

	checkForOverwrite(args.file, args.overwrite)

	tmp = tempfile.mkdtemp(dir=".")
	zipped = tempfile.mkdtemp(suffix=".zip", dir=".")
	execute(["rmdir", zipped], out=False)

	gatherPythonFiles(tmp)
	createMain(tmp)
	zip(zipped, tmp)
	addShebang(zipped, args.file)
	makeExecutable(args.file)
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Cleaning up temporary directories")
	cleanUp(tmp, zipped)


def checkForSudo():
	if not os.getuid() == 0:
		utils.out(utils.LINE_H, "build: ", utils.ERR, "Run with root privileges to integrate Ava with your system")
		utils.exit(silent=True)


def checkForOverwrite(out, canOverwrite):
	if os.path.exists(out):
		if canOverwrite:
			write = utils.booleanQuery(utils.LINE_H, "build: ", utils.BWARN, "File '" + out + "' will be written over. Would you like to continue?", default=False)
			if write:
				utils.out(utils.LINE_H, "build: ", utils.AFFIRM, "Removing '" + out + "'")
				cleanUp(out)
			else:
				utils.exit(silent=True)
		else:
			utils.out(utils.LINE_H, "build: ", utils.ERR, "File '" + out + "' already exists")
			utils.out(utils.LINE_H, "build: ", utils.ERR, "    Try running with the ", utils.CMD, "--overwrite", utils.ERR, " or ", utils.CMD, "-o", utils.ERR, " flag to write over the existing file")
			utils.exit(silent=True)


def gatherPythonFiles(tmp):
	cp = ["cp", "*.py", tmp]
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Gathering python files into the temporary directory")
	executeChecked(cp, shell=True)


def createMain(tmp):
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Creating '__main__.py' file")
	try:
		with open(os.path.join(tmp, "__main__.py"), "w+") as file:
			file.write("import ava\nif __name == '__main__':\n\tava")
	except EnvironmentError:
		utils.out(utils.LINE_H, "build: ", utils.ERR, "Could not create/write to '__main__.py' file")
		utils.exit(silent=True)


def zip(zipLoc, tmp):
	ZIP = ["zip",  "-r", zipLoc, "*"]
	MV_ZIP = ["mv", zipLoc, os.pardir]
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Zipping python files")
	executeChecked(ZIP, stdout=subprocess.PIPE, shell=True, cwd=tmp)
	executeChecked(MV_ZIP, shell=True, cwd=tmp)


def addShebang(zip, out):
	ECHO = ["echo", "#!/usr/bin/env python3"]
	CAT = ["cat", "-", zip, ">", out]
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Adding shebang to the zip")
	echod = executeChecked(ECHO, stdout=subprocess.PIPE)
	executeChecked(CAT, stdin=echod.stdout, shell=True)


def makeExecutable(out):
	CHMOD = ["chmod", "+x", out]
	utils.out(utils.LINE_H, "build: ", utils.STD_OUT, "Making '" + out + "' executable")
	executeChecked(CHMOD)


def cleanUp(*tmps, out=True):
	for tmp in tmps:
		executeChecked(["rm", "-rf", tmp], out=out)

build();
