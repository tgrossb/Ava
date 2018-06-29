###  This is pretty repetative, refactor later  ###
import utils
import os

def repairToolConfigFile():
	if not os.path.exists(utils.TOOL_CONFIG_PATH):
		makeToolConfigFile(utils.TOOL_DEFAULTS)
		return
	utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing tool configuration file at ", utils.TOOL_CONFIG_PATH, softest=utils.Q)
	config = utils.getConfigParser()
	config.read(utils.TOOL_CONFIG_PATH)
	repairedSections = 0
	repairedParams = 0
	for configLabel, default in utils.TOOL_DEFAULTS.items():
		if configLabel not in config.sections():
			config[configLabel] = {param: str(value) for param, value in default.items() }
			utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing section '" + configLabel + "' and all parameters using default values", softest=utils.N)
			repairedSections += 1
			for param, value in default.items():
				if not value == None:
					repairedParams += 1
			continue
		for param, value in default.items():
			if param not in config[configLabel]:
				if value == None:
					config.set(configLabel, param)
				else:
					config.set(configLabel, param, str(value))
					utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Repairing parameter '" + param + "' in section '" + configLabel + "' using default values", softest=utils.N)
					repairedParams += 1
	with open(utils.TOOL_CONFIG_PATH, 'w') as configFile:
		config.write(configFile)
	utils.out(utils.LINE_H, "ava: ", utils.AFFIRM, "Successfully repaired " + str(repairedParams) + " parameters in " + str(repairedSections) + " sections", softest=utils.Q)


def makeToolConfigFile(configMap):
	utils.out(utils.LINE_H, "ava: ", utils.STD_OUT, "Creating tool configuration file at ", utils.TOOL_CONFIG_PATH, softest=utils.Q)
	config = utils.getConfigParser()
	for configLabel, default in configMap.items():
		config[configLabel] = {}
		for param, value in default.items():
			config[configLabel][param] = str(value)
	configFile = open(utils.TOOL_CONFIG_PATH, 'w')
	config.write(configFile)
	configFile.close()


def readToolConfigs():
	if not os.path.exists(utils.TOOL_CONFIG_PATH):
		makeToolConfigFile(utils.TOOL_DEFAULTS)
	config = utils.getConfigParser()
	config.read(utils.TOOL_CONFIG_PATH)

	configs = {}
	missing = False
	for configLabel, default in utils.TOOL_DEFAULTS.items():
		configs[configLabel] = default
		if configLabel not in config.sections():
			utils.out(utils.LINE_H, "ava: ", utils.BWARN, "Using default values for missing section '" + configLabel + "'", softest=utils.N)
			missing = True
			continue
		for param, value in default.items():
			if value == None:
				continue
			if param not in config.options(configLabel):
				utils.out(utils.LINE_H, "ava: ", utils.BWARN, "Using default value for missing parameter '" + param + "' in section '" + configLabel + "'", softest=utils.N)
				missing = True
			else:
				configs[configLabel][param] = config.getboolean(configLabel, param) if isinstance(value, bool) else config.get(configLabel, param)
	if missing:
		utils.out(utils.LINE_H, "ava: ", utils.WARN, "Run with ", utils.CMD, "--repair-tool-config", utils.WARN, " or ", utils.CMD, "-r", utils.WARN, " to repair tool configurations", softest=utils.Q)
	return configs
