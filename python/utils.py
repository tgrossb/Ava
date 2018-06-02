#!/usr/bin/env python3
import subprocess
import os
import sys
import configparser
from collections import OrderedDict

def getConfigParser():
	parser = configparser.ConfigParser(allow_no_value = True, delimiters = ('='))
	parser.optionxform = str
	return parser


def out(*args, end="\n"):
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


def execute(cmd, stdout=subprocess.PIPE, stderr=None):
	out = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, universal_newlines=True)
	stream = out.stdout
	if stdout == None and not stderr == None:
		stream = out.stderr
	elif stdout == None and stderr == None:
		return
	for line in iter(stream.readline, ""):
		yield line
	stream.close()


def exit():
	out(HF, "Thank you for using the Ava Compiling and Executing Tool")
	sys.exit()


def inverseEscape(string):
	byteArr = string.encode("utf-8")
	return byteArr.decode("unicode_escape")


def replaceSymbol(sym, val, string):
	if string.startswith(sym):
#		print("Replacing '" + sym + "' with '" + val + "' in '" + string + "'  ==>  Joining '" + val + "' and '" + string[1:] + "'  ==>  Norming '" + os.path.join(val, string[1:]) + "'")
		return os.path.relpath(os.path.normpath(val + "/" + string[1:]))
	elif sym in string:
		out(LINE_H, "DEVELOPER ERROR: ", ERR, "Replace symbol gave out, have fun figuring this out, idiot")
		exit()
	return string


toolConfig = None

#########################################

PROJECT_CONFIG_NAME = "config.ini"
PROJECT = 'project'
PROJECT_NAME = 'project name'
HOME = 'project home'
HOME_SYM = '@'
CP = 'class path'
DEST = 'compiled destination'
RUN = 'runnable file'
COMPILE = 'compile files'

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

TOOL_CONFIG_PATH = os.getenv("HOME") + "/.ava.ini"

COLOR = 'color'
BOLD = 'bold'
TYPE = 'type'
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

PROJECT_LOGGING='project'
INDIVIDUAL_LOGGING='individual'
BOTH_LOGGING='both'
NONE_LOGGING='none'

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
		NAME: "ava.log"
	},
	LOGGING: {
		"# The type of logging": None,
		"# Log files store the stdout and stderr from each run": None,
		"# Options are": None,
		"#     " + PROJECT_LOGGING + ": logs are stored in the project home": None,
		"#     " + INDIVIDUAL_LOGGING + ": logs are stored in the directory where the command is run from": None,
		"#     " + BOTH_LOGGING + ": logs are stored in the project home and the directory where the command is run from": None,
		"#     " + NONE_LOGGING + ": logs are not created, and nothing is stored": None,
		TYPE: PROJECT_LOGGING
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

