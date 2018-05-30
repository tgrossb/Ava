#!/usr/bin/env python3
import toolConfig as ToolConfig
import projectConfig as ProjectConfig
import utils
import sys
import os
import argparse as ArgParser
import subprocess as SubProcess

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
	compResult = SubProcess.run(javac, stdout=SubProcess.DEVNULL, stderr=SubProcess.PIPE)
	if len(compResult.stderr) == 0:
		utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Compiled " + ", ".join([os.path.basename(file) for file in compileFiles])  + " without any errors")
	else:
		for line in compResult.stderr.decode("utf-8").splitlines():
			utils.out(utils.LINE_H, "ava: ", utils.ERR, line)
		utils.exit()

	java = ["java", "-cp", cp, projectConfig[utils.PROJECT][utils.MAIN]]
	utils.out(utils.LINE_H, "ava: ", utils.CMD, " ".join(java))

	utils.exit()


def main():
	# Get user configs and print the welcome message
	utils.out(utils.HF, "Welcome to the Ava Compiling and Executing Tool - Written by Theo Grossberndt")
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


def out(*args):
	utils.out(*args)


#########################################
# toolConfigs = None
###########################################

main()
