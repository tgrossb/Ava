###  This is pretty repetative, refactor later  ###
import utils
import sys
import os
from collections import OrderedDict

def makeProjectConfigFile(loc):
	utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Creating project configuration file at ", loc, softest=utils.Q)
	config = utils.getConfigParser()
	for configLabel, defaults in utils.PROJECT_DEFAULTS.items():
		config.add_section(configLabel)
		for param, value in defaults.items():
			if value == None:
				config.set(configLabel, param)
			else:
				config.set(configLabel, param, value)
	with open(loc, 'w') as configFile:
		config.write(configFile)


# Just is not ready, but I'll leave it here as a start
def repairProjectConfigFile(loc):
	if not os.path.exists(loc):
		makeProjectConfigFile(loc)
		return
	utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing project configuration file at ", loc)
	config = utils.getConfigParser()
	config.read(loc)
	repairedSections = 0
	repairedParams = 0
	for configLabel, default in utils.DEFAULTS.iteritems():
		if configLabel not in config.sections():
			config[configLabel] = {param: str(value).encode("string-escape") for param, value in default.iteritems() }
			utils.out(None, utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing section '" + configLabel + "' and all parameters using default values")
			repairedSections += 1
			repairedParams += len(default)
			continue
		for param, value in default.iteritems():
			if param not in config[configLabel]:
				config[configLabel][param] = str(value).encode("string-escape")
				utils.out(None, utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing parameter '" + param + "' in section '" + configLabel + "' using default values")
				repairedParams += 1
	configFile = open(utils.TOOL_CONFIG_PATH, 'w')
	config.write(configFile)
	configFile.close()
	utils.out(None, utils.LINE_H, "ava: ", utils.AFFIRM, "Successfully repaired " + str(repairedParameters) + " parameters in " + str(repairedSections) + " sections")


def readProjectConfigs(loc):
	config = utils.getConfigParser()
	config.read(loc)

	# Check first that the project section is defined
	if utils.PROJECT not in config.sections():
		utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project configuration file missing section '" + utils.PROJECT + "'", softest=utils.S)
		utils.exit()

	# Look for project home first so @ can be define
	at = "."
	if utils.HOME not in config.options(utils.PROJECT):
		utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project configuration file missing parameter '" + utils.HOME + "'", softest=utils.S)
		utils.exit()
	else:
		at = config.get(utils.PROJECT, utils.HOME)
		if utils.HOME_SYM in at:
			utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project home parameter contains home symbol (" + utils.HOME_SYM + ")", softest=utils.S)
			utils.exit()
		at = os.path.relpath(os.path.normpath(os.path.join(loc, os.pardir, at)))
	configs = OrderedDict()
	configs[utils.PROJECT] = OrderedDict()
	for param, value in utils.PROJECT_DEFAULTS[utils.PROJECT].items():
		if value == None:
			continue
		if param not in config.options(utils.PROJECT):
			utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project configuration file missing parameter '" + param + "'", softest=utils.S)
			utils.exit();
		userVal = str(config.get(utils.PROJECT, param))
		if utils.ALLOW_MULTIPLE_VALUES[param]:
			userVal = userVal.splitlines()
			for c in range(len(userVal)):
				userVal[c] = utils.replaceSymbol(utils.HOME_SYM, at, userVal[c])
				utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Adding " + userVal[c] + " as a value for parameter '" + param + "'", softest=utils.N)
		elif "\n" in userVal:
			utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project configuration file includes multiple values for single value parameter '" + param + "'", softest=utils.S)
			utils.exit()
		else:
			userVal = utils.replaceSymbol(utils.HOME_SYM, at, userVal)
			utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Recognized " + userVal + " as value for parameter '" + param + "'", softest=utils.N)
		configs[utils.PROJECT][param] = userVal
	return configs


def findProjectConfigFile(name):
	configLocation = '.'
	while not os.path.isfile(configLocation + '/' + name):
		if configLocation == '/':
			utils.out(utils.LINE_H, "ava: ", utils.ERR, "Project configuration file (", name, ") not found in parent directory", softest=utils.Q)
			utils.out(utils.LINE_H, "ava: ", utils.ERR, "Run with ", utils.CMD, "--make-project-config", utils.ERR, " or ", utils.CMD, "-m",
				utils.ERR, " to create a project configuration file", softest=utils.Q)
			utils.exit()
		configLocation = os.path.abspath(os.path.join(configLocation, os.pardir))
	return os.path.relpath(configLocation + '/' + name)
