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
	echo -e "${lih}updater: ${err}getopt --test failed"
	echo -e "${lih}updater: ${err}I'd try just doing the commands yourself"
	exit 2
fi

OPTIONS=c:o:e:a:l:s:b:
PARSED=$(getopt --options=$OPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
	echo -e "${lih}updater: ${err}getopt error, I don't know what happened"
	exit 3
fi
eval set -- "$PARSED"

while true; do
	case "$1" in
		-c)
			cmd="$nor$2"
			shift 2
			;;
		-o)
			out="$nor$2"
			shift 2
			;;
		-e)
			err="$nor$2"
			shift 2
			;;
		-a)
			aff="$nor$2"
			shift 2
			;;
		-l)
			lih="$nor$2"
			shift 2
			;;
		-s)
			std="$nor$2"
			shift 2
			;;
		-b)
			bwr="$nor$2"
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			echo -e "${lih}updater: ${err}I messed something up, let me know"
			exit 4
			;;
	esac
done

# Check for root
if [ "$EUID" -ne 0 ]; then
	echo -e "${lih}updater: ${err}This script must be run with root access"
	echo -e "${lih}updater: ${err}    /usr/local/bin requires root to write to"
	exit 5
fi

if [ -a "Ava" ]; then
	printf "${lih}updater: ${bwr}"
	read -p "Directory 'Ava' already exists. Would you like to write over it?(n) " yn
	case $yn in
		[Yy]*)
			sudo rm -rf Ava
			if [ $? -ne 0 ]; then
				echo -e "${lih}updater: ${cmd}sudo rm -rf Ava ${err}failed with exit code $?"
				exit 6
			fi
			;;
		[Nn]*)
			exit 1
			;;
		*)
			exit 1
			;;
	esac
fi
# GIT CLONE IS SO HARD TO DEAL WITH (it doesn't fully output when not to terminal)
# NOT OUTPUTING FOR THIS
printf "${lih}updater: ${cmd}git clone https://gitlab.com/tgrossb87/Ava.git ${std}... "
git clone https://gitlab.com/tgrossb87/Ava.git 2> /dev/null
if [ $? -ne 0 ]; then
	printf "${err}failed with exit code $?\n"
	exit 7
else
	printf "${aff}Done\n"
fi

cd Ava
if [ $? -ne 0 ]; then
	echo -e "${lih}updater: ${cmd}cd Ava ${err}failed with exit code $?"
	exit 8
fi

sudo ./build.sh -iw
if [ $? -eq 2 ]; then
	exit 1
elif [ $? -ne 0 ]; then
	echo -e "${lih}updater: ${cmd}sudo ./build.sh -iw ${err}failed with exit code $?"
	exit 9
fi

# Not going to check this one because it cannot fail
cd ..

sudo rm -rf Ava #|& while read r; do echo -e "${lih}updater: ${out}$r"; done #awk '{echo -e "${lih}updater: ${out}$1"}'
if [ $? -ne 0 ]; then
	echo "${lih}updater: ${cmd}sudo rm -rf Ava ${err}failed with exit code $?"
	exit 10
fi
echo -e "${lih}updater: ${aff}Ava has been updated and rebuilt successfully"
