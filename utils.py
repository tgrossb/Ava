#!/usr/bin/env python3
import subprocess
import os
import sys
import configparser
from datetime import datetime

def booleanQuery(*question, default=True):
	valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default:
		prompt = " [Y/n] "
	else:
		prompt = " [y/N] "

	while True:
		out(*question, prompt, end="")
		choice = input().lower()
		if default is not None and choice == '':
			return default
		elif choice in valid:
			return valid[choice]
		else:
			out("\r", end="")


def getConfigParser():
	parser = configparser.ConfigParser(allow_no_value = True, delimiters = ('='))
	parser.optionxform = str
	return parser


def out(*args, end="\n", softest = 0):
	if outputLevel < softest:
		return
	s = ""
	for arg in args:
		if not toolConfig == None and arg in TOOL_DEFAULTS:
			escaped = str((BOLDER if configs[arg][BOLD] else NORMALIZER) + toolConfig[arg][COLOR])
			s += inverseEscape(escaped)
		elif arg in TOOL_DEFAULTS:
			escaped = str((BOLDER if TOOL_DEFAULTS[arg][BOLD] else NORMALIZER) + TOOL_DEFAULTS[arg][COLOR])
			s += inverseEscape(escaped)
		else:
			s += str(arg)
	print(s, end=end)


def execute(cmd, stdout=subprocess.PIPE, stderr=None, shell=False, cwd=None):
	if not cwd == None:
		shell = True
	if shell and not isinstance(cmd, str):
		cmd = " ".join(cmd)
	out = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, universal_newlines=True, shell=shell, cwd=cwd)
	stream = out.stdout
	if stdout == None and not stderr == None:
		stream = out.stderr
	elif stdout == None and stderr == None:
		stream.close()
		return
	for line in iter(stream.readline, ""):
		yield line
	stream.close()


def openLog(configLoc, projectHome, javaCommand):
	global runningLog, projectLog, indivLog
	runningLog = "Run on " + str(datetime.now()) + " with command '" + javaCommand + "':"
	if toolConfigs[LOGGING][PROJECT_LOGGING]:
		projLogLoc = os.path.relpath(os.path.normpath(os.path.join(configLoc, os.pardir, projectHome, toolConfigs[LOG_NAME][NAME])))
		if not os.path.exists(projLogLoc):
			out(LINE_H, "ava: ", AFFIRM, "Creating project log file at " + projLogLoc)
			projectLog = open(projLogLoc, 'w+')
		else:
			out(LINE_H, "ava: ", AFFIRM, "Using project log file at " + projLogLoc)
			projectLog = open(projLogLoc, 'r+')
	if toolConfigs[LOGGING][INDIVIDUAL_LOGGING]:
		indivLogLoc = toolConfigs[LOG_NAME][NAME]
		dotLoc = indivLogLoc.index(".")
		counter = 1
		while os.path.exists(indivLogLoc[:dotLoc] + str(counter) + indivLogLoc[dotLoc:]):
			counter += 1
		indivLogLoc = indivLogLoc[:dotLoc] + str(counter) + indivLogLoc[dotLoc:]
		out(LINE_H, "ava: ", AFFIRM, "Creating individual log file at " + indivLogLoc)
		indivLog = open(indivLogLoc, 'w')


def log(line):
	global runningLog
	runningLog += "\n\t" + line.rstrip().replace("\n", "\n\t")


def closeLog():
	if not projectLog == None:
		content = runningLog + "\n\n" + projectLog.read()
		projectLog.seek(0, 0)
		projectLog.write(content.rstrip())
		projectLog.close()
	if not indivLog == None:
		indivLog.write(runningLog)
		indivLog.close()


def prependToFile(startLine, lines, fileLocation):
	with open(fileLocation, 'r+') as file:
		content = file.read()
		file.seek(0, 0)
		file.write(startLine)
		file.write("\t" + lines.replace("\n", "\n\t").rstrip() + "\n\n" + content)


def exit(silent=False):
	if not silent:
		out(HF, "Thank you for using the Ava Compiling and Executing Tool")
	sys.exit()


def inverseEscape(string):
	byteArr = string.encode("utf-8")
	return byteArr.decode("unicode_escape")


def replaceSymbol(sym, val, string, start=os.curdir):
	if string.startswith(sym):
#		print("Replacing '" + sym + "' with '" + val + "' in '" + string + "'  ==>  Joining '" + val + "' and '" + string[1:] + "'  ==>  Norming '" + os.path.join(val, string[1:]) + "'")
		return os.path.relpath(os.path.normpath(val + "/" + string[1:]), start=start)
	elif sym in string:
		out(LINE_H, "DEVELOPER ERROR: ", ERR, "Replace symbol finally gave out, have fun figuring this out, idiot")
		exit()
	return string


outputLevel = None
toolConfig = None
runningLog = None
projectLog, indivLog = None, None

#########################################

V = 1   # Verbose output
N = 0   # Normal output
Q = -1  # Quiet output
S = -2  # Silent output

#########################################

PROJECT = 'project'
PROJECT_NAME = 'project name'
HOME = 'project home'
HOME_SYM = '@'
CP = 'class path'
DEST = 'compiled destination'
RUN = 'runnable file'
COMPILE = 'compile files'
REL_HOME = 'dont display'

PROJECT_DEFAULTS = {
	PROJECT: {
		"# The name of this project": None,
		PROJECT_NAME: "My Project\n",
		"# The home director for the project, can be relative to this file or absolute": None,
		"# This variable can be refered to as '" + HOME_SYM + "' in the rest of the config file": None,
		HOME: ".\n",
		"# The paths to any external files (.jar) to be compiled, non jar files will be ignored": None,
		"# External files can be refrenced individually and put on individual lines or with wildcards": None,
		CP: "@/libs/*\n@/libs/a-sweet-library.jar\n",
		"# The destination for compiled (.bin) files": None,
		DEST: "@/bin\n",
		"# The main, runnable file that includes a main(String[] args) function": None,
		RUN: "com.root.Main\n",
		"# The paths to each file that needs to be compiled, in any order": None,
		COMPILE: "@/src/com/root/Main.java\n@/src/com/root/utils/Utils.java"
	}
}

#########################################

TOOL_CONFIG_PATH = os.getenv('HOME') + '/.ava.ini'

COLOR = 'color'
BOLD = 'bold'
NAME = 'name'

HF = 'header/footer'
CMD = 'command'
OUT = 'command output'
WARN = 'warning'
BWARN = 'background warning'
ERR = 'error'
AFFIRM = 'affirmation'
LINE_H = 'line header'
STD_OUT = 'standard output'
LOG_NAME = 'log file name'
LOGGING = 'logging type'

NORMALIZER = '\\033[21m'
BOLDER = NORMALIZER + '\\033[1m'

PROJECT_LOGGING='project logging'
INDIVIDUAL_LOGGING='individual logging'

PROJECT_CONFIG = 'project configuration file'

TOOL_DEFAULTS = {
	HF: {
		"# Color of the header and footer text": None,
		"# This is used when the tool starts and finishes": None,
		COLOR: '\\033[95m',
		BOLD: False
	},
	CMD: {
		"# Color of the executed commands": None,
		"# This is used to reflect the commands the tool runs": None,
		COLOR: '\\033[94m',
		BOLD: False
	},
	OUT: {
		"# Color of the outputs": None,
		"# This is the color used when your program prints": None,
		COLOR: '\\033[37m',
		BOLD: False
	},
	WARN: {
		"# Color of important warning outputs": None,
		COLOR: '\\033[93m',
		BOLD: False
	},
	BWARN: {
		"# Color of background warning outputs": None,
		"# This is used for informational warnings that support important warnings": None,
		COLOR: '\\033[33m',
		BOLD: False
	},
	ERR: {
		"# Color of the error outputs": None,
		COLOR: '\\033[91m',
		BOLD: True
	},
	AFFIRM: {
		"# Color of affirmation outputs": None,
		"# This is used for statements confirming actions or values": None,
		COLOR: '\\033[92m',
		BOLD: False
	},
	LINE_H: {
		"# Color of line headers": None,
		COLOR: '\\033[97m',
		BOLD: True
	},
	STD_OUT: {
		"# Color of standard output": None,
		"# This is used for basic output created by the tool, not your program": None,
		COLOR: '\\033[97m',
		BOLD: False
	},
	LOG_NAME: {
		"# The name of the file where logs are stored": None,
		"# This should not be a path, as the actual location will change": None,
		NAME: "log.ava"
	},
	LOGGING: {
		"# The type of logging": None,
		"# Log files store the stdout and stderr from each run": None,
		"# Options are": None,
		"#     " + PROJECT_LOGGING + ": logs are stored in the project home": None,
		"#     " + INDIVIDUAL_LOGGING + ": logs are stored in the directory where the command is run from": None,
		"# Each parameter is a boolean": None,
		"# Mark one, both, or none as true to store logs in that style": None,
		PROJECT_LOGGING: True,
		INDIVIDUAL_LOGGING: False
	},
	PROJECT_CONFIG: {
		"# The name of the project configuration file": None,
		"# This is what ava will search for and create by default when the -m flag is used": None,
		NAME: 'config.ini'
	}
}

#########################################

ALLOW_MULTIPLE_VALUES = {
	PROJECT_NAME: False,
	HOME: False,
	CP: True,
	DEST: False,
	RUN: False,
	COMPILE: True
}

###########################################

TOOL_DESCRIPTION = 'This tool can be used to compile and run Java programs from the command line using a project configuration file. This allows you to use a single, simple command ' +\
			'to compile and run an entire project. This tool can handle everything from external libraries to complex package structures.'
TOOL_EPILOG = 'This tool uses ini files for configuration, so you only need to input your information into the project configuration file once (automatic generation coming soon), ' +\
			'and then running is as easy as running this program.'
