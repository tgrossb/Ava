#!/bin/bash

nor="\033[21m"
cmd="$nor\033[94m"
out="$nor\033[37m"
err="$nor\033[1m\033[91m"
aff="$nor\033[92m"
lih="$nor\033[1m\033[97m"
std="$nor\033[97m"
bwr="$nor\033[33m"

# Got to parse for the export and help flags
getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
	echo -e "${lih}build: ${cmd}getopt --test ${err}failed with exit code $?"
	echo -e "${lih}build: ${err}    I'd try just doing the commands yourself"
	exit 1
fi

OPTIONS=ihf:wc:o:e:a:l:s:b:
LONGOPTIONS=integrate,help,file:,write

PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
	exit 2
fi
eval set -- "$PARSED"

while true; do
	case "$1" in
		-i|--integrate)
			i=y
			shift
			;;
		-h|--help)
			h=y
			shift
			;;
		-w|--write)
			w=y
			shift
			;;
		-f|--file)
			outFile="$2"
			shift 2
			;;
		-c)
			cmd="$2"
			shift 2
			;;
		-o)
			out="$2"
			shift 2
			;;
		-e)
			err="$2"
			shift 2
			;;
		-a)
			aff="$2"
			shift 2
			;;
		-l)
			lih="$2"
			shift 2
			;;
		-s)
			std="$2"
			shift 2
			;;
		-b)
			bwr="$2"
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			printf "Error: I messed something up, let me know\n"
			exit 1
			;;
	esac
done

# Check for help
if [ $h ]; then
	echo "This is a simple tool used to create a single runnable from all of the python files in this directory"
	echo "Options:"
	echo "    --output, -o:     The name of the file to generate"
	echo "    --integrate, -i:  Integrate the tool with your system"
	echo "                      Export the generated runnable to the /usr/local/bin file (requires root)"
	echo "    --write, -w:      Write over existing files if requred, confirming before writing"
	echo "    --help, -h:       Display this help output"
	exit 0
fi

# Check for output file arg length
if [[ ! $outFile ]]; then
	printf "Using default value 'ava' for output file\n"
	outFile="ava"
#	printf "Error: No output file was defined with the --output or -o parameter\n"
#	printf "       Trying running with the --help or -h flag for help\n"
#	exit 4
fi

# If the user didn't use -i, make sure they don't want to
if [ ! $i ]; then
	read -p "Warning: You ran this script without the -i flag. Are you sure you want to do this?
		Answering 'yes' will continue without integrating.
		Answering 'no' will integrate the command.(n) " yn
	case $yn in
		[Yy]*)
			printf "Continuing without integration\n"
			;;
		[Nn]*)
			printf "Now integrating the command with your system\n"
			i=y
			;;
		*)
			printf "Now integrating the command with your system\n"
			i=y
			;;
	esac
fi

# Check for root if it being integrated
if [ $i ] && [ "$EUID" -ne 0 ]; then
	printf "Error: Run with root to integrate with the system\n"
	printf "       /usr/local/bin requires root to write to\n"
	exit 4
fi

# If it is being integrated, make the out file /usr/local/bin/<outFile name>
if [ $i ]; then
	outFile=$(basename -- "$outFile")
	outFile="/usr/local/bin/$outFile"
fi

# Check if output file exists already
if [ -a "$outFile" ]; then
	if [ $w ]; then
		read -p "File '$outFile' will be written over. Would you like to continue?(n) " yn
		case $yn in
			[Yy]*)
				printf "Removing '$outFile'..."
				rm $outFile
				printf " Done\n"
				;;
			[Nn]*)
				printf "Alright, stopping everything.. Done\n"
				exit 0
				;;
			*)
				printf "Alright, stopping everything... Done\n"
				exit 0
				;;
		esac
	else
		printf "Error: File '$outFile' already exists\n"
		printf "       Try running with the --write or -w flag to write over existing files\n"
		exit 4
	fi
fi

# Set up the directory and add the __main__.py
printf "Creating temporary directory..."
dir=`mktemp -d -p $(pwd)`
if [[ ! "$dir" ]]; then
	printf "Error: Could not create temporary directory\n"
	exit 1
fi
printf " Done\n"
printf "Gathering python files into the temporary directory..."
cp *.py $dir
printf " Done\n"
cd $dir
printf "Creating '__main__.py' file..."
printf "import ava\nif __name__ == '__main__':\n\tava" > __main__.py
printf " Done\n"

# Make the actual executable
printf "Creating temporary zip file..."
zipped=`mktemp -d -p $(dirname -- "$dir") --suffix=".zip"`
if [[ ! "$zipped" ]]; then
	printf "\nError: Could not create temporary zipped directory\n"
	exit 1
fi
printf " Done\n"
# Remove the created directory - we just want the name and zip will make it
rmdir $zipped
printf "Zipping python files..."
zip -r $zipped * &> /dev/null && cd ..
printf " Done\nMaking runnable '$outFile' from temporary zipped file..."
echo '#!/usr/bin/env python3' | cat - $zipped > $outFile
chmod +x $outFile
printf " Done\n"

# Clean up
printf "Cleaning up temporary files..."
rm -rf $zipped
rm -rf $dir
printf " Done\n"

# Move the output to the /usr/local/tmp if indicated
if [ $i ]; then
	printf "Ava has been built successfully, and is now integrated with your system\n"
	printf "The tool can now be run with the command $(basename -- $outFile)\n"
else
	printf "Ava has been built successfully\n"
	printf "Use the -i or --integrate flag to integrate the tool with your system\n"
fi
