#!/usr/bin/env python3
import toolConfig as ToolConfig
import projectConfig as ProjectConfig
import utils
import os
import argparse as ArgParser
import subprocess as SubProcess
import re

def parseArgs():
	argParser = ArgParser.ArgumentParser()
	argParser.add_argument('-m', '--make', action='store_true')
	argParser.add_argument('-q', '--quiet', action='store_true')
	argParser.add_argument('-s', '--silent', action='store_true')
	argParser.add_argument('-r', '--repair-tool-config', action='store_true')
	return argParser.parse_args()


def ava():
	# Get project config
	configLoc = ProjectConfig.findProjectConfigFile(utils.PROJECT_CONFIG_NAME)
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Using project configuration file at ", configLoc)
	projectConfig = ProjectConfig.readProjectConfigs(configLoc)
	dest = projectConfig[utils.PROJECT][utils.DEST]
	cp = dest
	for path in projectConfig[utils.PROJECT][utils.CP]:
		cp += ":" + path
	compileFiles = projectConfig[utils.PROJECT][utils.COMPILE]

	javac = ["javac", "-cp", cp, "-d", dest, *compileFiles]
	utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(javac))
	errLines = 0
	for line in utils.execute(javac, stdout=None, stderr=SubProcess.PIPE):
		utils.out(utils.LINE_H, "javac: ", utils.ERR, line, end="")
		errLines += 1
	if errLines == 0:
		utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Compiled " + ", ".join([os.path.basename(file) for file in compileFiles])  + " without any errors")
	else:
		utils.exit()

	java = ["java", "-cp", cp, projectConfig[utils.PROJECT][utils.RUN]]
	utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(java))
	exceptionMatcher = re.compile(r"^.*Exception[^\n]+(\s+at [^\n]+)*\s*\Z", re.MULTILINE | re.DOTALL)
	runningLine = ""
#	utils.openLog(configLoc, projectConfig[utils.PROJECT][utils.HOME], " ".join(java))
	for line in utils.execute(java, stderr=SubProcess.STDOUT):
		runningLine += line
		outputColor = utils.ERR if exceptionMatcher.match(runningLine) else utils.OUT
		utils.out(utils.LINE_H, "java: ", outputColor, line, end="")
		utils.oldLog(line, configLoc, projectConfig[utils.PROJECT][utils.HOME], " ".join(java))
#	utils.closeLog()
	utils.exit()


def main():
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
	utils.out(utils.inverseEscape(headerColor) + "Welcome to the Ava Compiling and Executing Tool - Written by Theo Grossberndt")
	args = parseArgs()

	# Reapir tool configuration file, then exit
	# This is the only one that comes before getting and using the tool config
	if args.repair_tool_config:
		ToolConfig.repairToolConfigFile()
		utils.exit()

	utils.toolConfigs = ToolConfig.readToolConfigs()
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Using tool configuration file at ", utils.TOOL_CONFIG_PATH)

	# Make a project configuration file where the command is run, then exit
	if args.make:
		ProjectConfig.makeProjectConfigFile("./" + utils.PROJECT_CONFIG_NAME)
		utils.exit()

	ava()

try:
	main()
except KeyboardInterrupt:
	utils.closeLog()
	utils.exit()
