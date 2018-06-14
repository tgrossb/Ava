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
	exit 3
fi

OPTIONS=ihf:wc:o:e:a:l:s:b:
LONGOPTIONS=integrate,help,file:,write

PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
	echo -e "${lih}build: ${err}getopt error, I don't know what happened"
	exit 4
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
			echo -e "${lih}build: ${err}I messed something up, let me know"
			exit 5
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
	echo -e "${lih}build: ${std}Using default value 'ava' for output file"
	outFile="ava"
#	printf "Error: No output file was defined with the --output or -o parameter\n"
#	printf "       Trying running with the --help or -h flag for help\n"
#	exit 4
fi

# If the user didn't use -i, make sure they don't want to
if [ ! $i ]; then
	echo -e "${lih}build: ${bwr}You ran this script without the -i flag. Are you sure you want to do this?"
	echo -e "${lih}build: ${bwr}    Answering 'yes' will continue without integrating."
	printf "${lih}build: ${bwr}    Answering 'no' will integrate the command.(n) "
	read yn
	case $yn in
		[Yy]*)
			echo -e "${lih}build: ${aff}Continuing without integration"
			;;
		[Nn]*)
			echo -e "${lih}build: ${aff}Now integrating the command with your system"
			i=y
			;;
		*)
			echo -e "${lih}build: ${aff}Now integrating the command with your system"
			i=y
			;;
	esac
fi

# Check for root if it being integrated
if [ $i ] && [ "$EUID" -ne 0 ]; then
	echo -e "${lih}build: ${err}Run with root to integrate with the system"
	exit 6
fi

# If it is being integrated, make the out file /usr/local/bin/<outFile name>
if [ $i ]; then
	outFile=$(basename -- "$outFile")
	outFile="/usr/local/bin/$outFile"
fi

# Check if output file exists already
if [[ -a "$outFile" ]]; then
	if [ $w ]; then
		printf "${lih}build: ${bwr}File '$outFile' will be written over. Would you like to continue?(n) "
		read yn
		case $yn in
			[Yy]*)
				printf  "${lih}build: ${std}Removing '$outFile'..."
				rm $outFile
				printf " ${aff}Done\n"
				;;
			[Nn]*)
				printf "${lih}build: ${std}Alright, stopping everything... ${aff}Done\n"
				exit 2
				;;
			*)
				printf "${lih}build: ${std}Alright, stopping everything... ${aff}Done\n"
				exit 2
				;;
		esac
	else
		echo -e "${lih}build: ${err}File '$outFile' already exists"
		echo -e "${lih}build: ${err}    Try running with the --write or -w flag to write over existing files"
		exit 7
	fi
fi

# Set up the directory and add the __main__.py
printf "${lih}build: ${std}Creating temporary directory..."
dir=`mktemp -d -p $(pwd)`
if [[ ! "$dir" ]]; then
	printf "\n${lih}build: ${err}Could not create temporary directory"
	exit 8
fi
printf " ${aff}Done\n"
printf "${lih}build: ${std}Gathering python and updater files into the temporary directory..."
cp *.py update.sh $dir
printf " ${aff}Done\n"
cd $dir
printf "${lih}build: ${std}Creating '__main__.py' file..."
printf "import ava\nif __name__ == '__main__':\n\tava" > __main__.py
printf " ${aff}Done\n"

# Make the actual executable
printf "${lih}build: ${std}Creating temporary zip file..."
zipped=`mktemp -d -p $(dirname -- "$dir") --suffix=".zip"`
if [[ ! "$zipped" ]]; then
	printf "\n${lih}build: ${err}Could not create temporary zipped directory\n"
	exit 9
fi
printf " ${aff}Done\n"
# Remove the created directory - we just want the name and zip will make it
rmdir $zipped
printf "${lih}build: ${std}Zipping python files..."
zip -r $zipped * &> /dev/null && cd ..
printf " ${aff}Done\n${lih}build: ${std}Making runnable '$outFile' from temporary zipped file..."
echo '#!/usr/bin/env python3' | cat - $zipped > $outFile
chmod +x $outFile
printf " ${aff}Done\n"

# Clean up
printf "${lih}build: ${std}Cleaning up temporary files..."
rm -rf $zipped
rm -rf $dir
printf " ${aff}Done\n"

# Show the integrated or not messsages
if [ $i ]; then
	printf "${lih}build: ${aff}Ava has been built successfully, and is now integrated with your system\n"
	printf "${lih}build: ${aff}The tool can now be run with the command ${cmd}$(basename -- $outFile)\n"
	exit 0
else
	printf "${lih}build: ${aff}Ava has been built successfully\n"
	printf "${lih}build: ${std}Use the ${cmd}-i ${std}or ${cmd}--integrate ${std}flag to integrate the tool with your system\n"
	exit 1
fi
