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
NAME = 'project name'
HOME = 'project home'
HOME_SYM = '@'
CP = 'class path'
DEST = 'compiled destination'
RUN = 'runnable file'
COMPILE = 'compile files'
PROJECT_DEFAULTS = OrderedDict()
PROJECT_DEFAULTS[PROJECT] = OrderedDict()
PROJECT_DEFAULTS[PROJECT]["# The name of this project"] = None
PROJECT_DEFAULTS[PROJECT][NAME] = "My Project\n"
PROJECT_DEFAULTS[PROJECT]["# The home director for the project, can be relative to this file or absolute"] = None
PROJECT_DEFAULTS[PROJECT]["# This variable can be refered to as '" + HOME_SYM + "' in the rest of the config file"] = None
PROJECT_DEFAULTS[PROJECT][HOME] = ".\n"
PROJECT_DEFAULTS[PROJECT]["# The paths to any external files (.jar) to be compiled, non jar files will be ignored"] = None
PROJECT_DEFAULTS[PROJECT]["# External files can be refrenced individually and put on individual lines or with wildcards"] = None
PROJECT_DEFAULTS[PROJECT][CP] = "@/libs/*\n@/libs/a-sweet-library.jar\n"
PROJECT_DEFAULTS[PROJECT]["# The destination for compiled (.bin) files"] = None
PROJECT_DEFAULTS[PROJECT][DEST] = "@/bin\n"
PROJECT_DEFAULTS[PROJECT]["# The main, runnable file that includes a main(String[] args) function"] = None
PROJECT_DEFAULTS[PROJECT][RUN] = "com.root.Main\n"
PROJECT_DEFAULTS[PROJECT]["# The paths to each file that needs to be compiled, in any order"] = None
PROJECT_DEFAULTS[PROJECT][COMPILE] = "@/src/com/root/Main.java\n@/src/com/root/utils/Utils.java"

#########################################

TOOL_CONFIG_PATH = os.getenv("HOME") + "/.ava.ini"
COLOR = 'color'
BOLD = 'bold'
TYPE = 'type'
HF = 'header/footer'
CMD = 'command'
OUT = 'command output'
WARN = 'warning'
BWARN = 'background warning'
ERR = 'error'
AFFIRM = 'affirmation'
LINE_H = 'line header'
STD_OUT = 'standard output'
LOG = 'logging'
NORMALIZER = '\\033[21m'
BOLDER = NORMALIZER + '\\033[1m'
TOOL_DEFAULTS = OrderedDict()
TOOL_DEFAULTS[HF] = OrderedDict()
TOOL_DEFAULTS[HF][COLOR] = '\\033[95m'
TOOL_DEFAULTS[HF][BOLD] = False
TOOL_DEFAULTS[CMD] = OrderedDict()
TOOL_DEFAULTS[CMD][COLOR] = '\\033[94m'
TOOL_DEFAULTS[CMD][BOLD] = False
TOOL_DEFAULTS[OUT] = OrderedDict()
TOOL_DEFAULTS[OUT][COLOR] = '\\033[37m'
TOOL_DEFAULTS[OUT][BOLD] = False
TOOL_DEFAULTS[WARN] = OrderedDict()
TOOL_DEFAULTS[WARN][COLOR] = '\\033[93m'
TOOL_DEFAULTS[WARN][BOLD] = False
TOOL_DEFAULTS[BWARN] = OrderedDict()
TOOL_DEFAULTS[BWARN][COLOR] = '\\033[33m'
TOOL_DEFAULTS[BWARN][BOLD] =  False
TOOL_DEFAULTS[ERR] = OrderedDict()
TOOL_DEFAULTS[ERR][COLOR] = '\\033[91m'
TOOL_DEFAULTS[ERR][BOLD] = True
TOOL_DEFAULTS[AFFIRM] = OrderedDict()
TOOL_DEFAULTS[AFFIRM][COLOR] = '\\033[92m'
TOOL_DEFAULTS[AFFIRM][BOLD] = False
TOOL_DEFAULTS[LINE_H] = OrderedDict()
TOOL_DEFAULTS[LINE_H][COLOR] =  '\\033[97m'
TOOL_DEFAULTS[LINE_H][BOLD] = True
TOOL_DEFAULTS[STD_OUT] = OrderedDict()
TOOL_DEFAULTS[STD_OUT][COLOR] = '\\033[97m'
TOOL_DEFAULTS[STD_OUT][BOLD] =False
TOOL_DEFAULTS[LOG] = OrderedDict()
TOOL_DEFAULTS[LOG][TYPE] = 'project'

#########################################

ALLOW_MULTIPLE_VALUES = {
	NAME: False,
	HOME: False,
	CP: True,
	DEST: False,
	RUN: False,
	COMPILE: True
}

###########################################
