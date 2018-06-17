#!/usr/bin/env python3
import toolConfig as ToolConfig
import projectConfig as ProjectConfig
import utils
import os
import argparse as ArgParser
import subprocess as SubProcess
import re

def parseArgs():
	argParser = ArgParser.ArgumentParser(prog='ava', description=utils.TOOL_DESCRIPTION, epilog=utils.TOOL_EPILOG)
	argParser.add_argument('-m', '--make', action='store_true', help='make a project configuration file in the current directory, and populate the configuration file with examples')
	argParser.add_argument('-e', '--edit', action='store_true', help="edit the current project's configuration file")
	argParser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
	argParser.add_argument('-q', '--quiet', action='store_true', help='enable quiet output')
	argParser.add_argument('-s', '--silent', action='store_true', help='enable silent output')
	argParser.add_argument('-r', '--repair-tool', action='store_true', help='repair the configuration file for the tool by filling in any missing or incomplete sections')
	argParser.add_argument('-u', '--update', action='store_true', help='update the tool to the latest release version')
	argParser.add_argument('parameters', nargs='*', help='a list of parameters to pass to the java command')
	return argParser.parse_args()



def update():
	utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Updating the ava tool")
	updater = ["sudo", "./update.sh"]
	utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(updater))
	SubProcess.call(updater)
#	for line in utils.execute(updater, stderr=SubProcess.STDOUT, shell=True):
#		utils.out(utils.LINE_H, "update: ", utils.OUT, line, end="")
#	git = ["git", "clone", "https://gitlab.com/tgrossb87/Ava.git"]
#	build = ["cd", "Ava", "&&", "sudo", "./build", "-iw"]
#	clean = ["rm", "-rf", "Ava"]
#	git = "git clone https://gitlab.com/tgrossb87/Ava.git"
#	build = "cd Ava && sudo ./build -iw"
#	clean = "rm -rf Ava"
#	utils.out(utils.LINE_H, "ava: ", utils.CMD, git)#" ".join(git))
#	for line in utils.execute(git, stderr=SubProcess.STDOUT, shell=True):
#		utils.out(utils.LINE_H, "git: ", utils.OUT, line, end="")
#	utils.out(utils.LINE_H, "ava: ", utils.CMD, build)#" ".join(build))
#	for line in utils.execute(build, stderr=SubProcess.STDOUT, shell=True):
#		utils.out(utils.LINE_H, "build: ", utils.OUT, line, end="")
#	utils.out(utils.LINE_H, "ava: ", utils.CMD, clean)#" ".join(clean))
#	for line in utils.execute(clean, stderr=SubProcess.STDOUT, shell=True):
#		utils.out(utils.LINE_H, "clean: ", utils.OUT, line, end="")
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Ava has been successfully updated!")


def ava(configLoc, javaParams):
	projectConfig = ProjectConfig.readProjectConfigs(configLoc)
	dest = projectConfig[utils.PROJECT][utils.DEST]
	cp = dest
	for path in projectConfig[utils.PROJECT][utils.CP]:
		cp += ":" + path
	compileFiles = projectConfig[utils.PROJECT][utils.COMPILE]

	javac = ["javac", "-cp", cp, "-d", dest, *compileFiles]
	utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(javac), softest=utils.Q)
	errLines = 0
	for line in utils.execute(javac, stdout=None, stderr=SubProcess.PIPE):
		utils.out(utils.LINE_H, "javac: ", utils.ERR, line, end="", softest=utils.S)
		errLines += 1
	if errLines == 0:
		utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Compiled " + ", ".join([os.path.basename(file) for file in compileFiles])  + " without any errors", softest=utils.Q)
	else:
		utils.exit()

	java = ["java", "-cp", cp, projectConfig[utils.PROJECT][utils.RUN], *javaParams]
	javaString = " ".join(java)
	utils.out(utils.LINE_H, "ava: ", utils.CMD, javaString, softest=utils.Q)
	exceptionMatcher = re.compile(r"^.*Exception[^\n]+(\s+at [^\n]+)*\s*\Z", re.MULTILINE | re.DOTALL)
	runningLine = ""
	utils.openLog(configLoc, projectConfig[utils.PROJECT][utils.HOME], javaString)
	for line in utils.execute(java, stderr=SubProcess.STDOUT):
		runningLine += line
		outputColor = utils.ERR if exceptionMatcher.match(runningLine) else utils.OUT
		utils.out(utils.LINE_H, "java: ", outputColor, line, end="", softest=utils.S)
		utils.log(line)
	utils.closeLog()
	utils.exit()


def main(args):
	# Look ahead to the tool config file to get header color
	headerColorDefault = utils.TOOL_DEFAULTS[utils.HF][utils.COLOR]
	headerBoldDefault = utils.TOOL_DEFAULTS[utils.HF][utils.BOLD]
	headerColor = (utils.BOLDER if headerBoldDefault else "") + headerColorDefault
	configParser = utils.getConfigParser()
	if os.path.exists(utils.TOOL_CONFIG_PATH):
		configParser.read(utils.TOOL_CONFIG_PATH)
		headerColor = configParser.get(utils.HF, utils.COLOR, fallback=headerColorDefault)
		if configParser.getboolean(utils.HF, utils.BOLD, fallback=headerBoldDefault):
			headerColor = utils.BOLDER + headerColor

	# Get user configs and print the welcome message
	utils.out(utils.inverseEscape(headerColor) + "Welcome to the Ava Compiling and Executing Tool - Written by Theo Grossberndt", softest=utils.S)

	# Reapir tool configuration file, then exit
	# This is the only one that comes before getting and using the tool config
	if args.repair_tool:
		ToolConfig.repairToolConfigFile()
		utils.exit()

	utils.toolConfigs = ToolConfig.readToolConfigs()
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Using tool configuration file at ", utils.TOOL_CONFIG_PATH, softest=utils.Q)

	# Update is now the first priority
	if args.update:
		update()
		utils.exit()

	# Make a project configuration file where the command is run, then exit
	if args.make:
		ProjectConfig.makeProjectConfigFile("./" + utils.toolConfigs[utils.PROJECT_CONFIG][utils.NAME])
		utils.exit()

	projectConfigLoc = ProjectConfig.findProjectConfigFile(utils.toolConfigs[utils.PROJECT_CONFIG][utils.NAME])
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Using project configuration file at ", projectConfigLoc, softest=utils.Q)
	if args.edit:
		editor = os.getenv("EDITOR")
		if editor == None:
			utils.out(utils.LINE_H, "ava: ", utils.WARN, "The environment variable $EDITOR not defined, using nano by default")
			editor = "nano"
		edit = [editor, projectConfigLoc]
		utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(edit), softest=utils.Q)
		SubProcess.call(edit)
		utils.exit()
	ava(projectConfigLoc, args.parameters)

try:
	args = parseArgs()
	if args.verbose:
		utils.outputLevel = utils.V
	elif args.quiet:
		utils.outputLevel = utils.Q
	elif args.silent:
		utils.outputLevel = utils.S
	else:
		utils.outputLevel = utils.N
	main(args)
except KeyboardInterrupt:
	utils.closeLog()
	utils.exit()
