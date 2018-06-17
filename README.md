## Ava ##
This is unpackaged source for the Ava Compiling and Executing tool, or ava for short.  This tool was created to simplify compiling and running Java programs from the command line.  It simplifies 
compiling multiple files organized into packages and is able to export compiled files into seperate directories.  Feel free to download and use or modify this tool for easy use.

## Installing ##
Installing this tool is fairly easy. All you need to do is download the dependencies and then follow the instructions in the Building section of the README. Eventually, I'll setup an even easier way 
to install and build.

## Dependencies ##
Before downloading and building this tool, some dependencies need to be installed.<br/>
Git:
```bash
sudo apt-get install git
```
Python 3 and pip3:
```bash
sudo apt-get install python3 python3-pip
```
<a href="https://docs.python.org/3/library/configparser.html">Config Parser</a>
```bash
pip3 install configparser
```

## Building ##
To build this tool, you can use the simple bash script I wrote to create a single runnable. Or, of course, if you're hard core you can build it yourself. Both options 
are here.<br/>
**This is the easy way to build, by using the build tool**:
```bash
git clone https://gitlab.com/tgrossb87/Ava.git
cd Ava
sudo ./build.py -io
```
This will use the `build` tool to compile all of the python files into a zipped folder and export it as a runnable to `/usr/local/bin/ava` so the command `ava` can be used from anywhere.<br/>
After this, you can remove the repository if you would like:
```bash
cd ..
rm -rf Ava
```
Or, if you really want, you could build it yourself:
```bash
git clone https://gitlab.com/tgrossb87/Ava.git
cd Ava
mkdir avaRelease
cp *.py avaRelease
cd avaRelease
touch __main__.py
printf "import ava\nif __name__=='__main__':\n\tava" > __main__.py
zip -r ../inter.zip * && cd ..
echo '#!/usr/bin/env python3' | cat - inter.zip > ava
chmod +x ava
rm -rf avaRelease
rm inter.zip
sudo mv ava /usr/local/bin
```
This will create a runnable file called `ava` that you move to the `/usr/local/bin` directory. Alternatively, you could place the `ava` executable anywhere you want and add this path 
to your `PATH` variable. I would recommend using the tool though, its much easier.  You can then remove the repository as above if you would like.

## Features ##
- [X] Named projects
- [X] Multiple and parallel file compiling
- [X] Automatic running
- [X] Project and individual logging options
- [X] Command piping to log file - Kind of
- [X] External library compiling available
- [X] Color and logging per user configurations
- [X] Automatic tool and project configuration file generation
- [ ] Intelligent project configuration generation
- [ ] Clickable error output to take the user to the error (this is a terminal problem, might be a long shot)
- [X] Normal, verbose, quiet, and silent output options
- [ ] Integrated version control (maybe)
- [X] Configuration file look ahead
- [X] Error highlighting in `java` command output
- [X] Integrated project configuration file editing
- [ ] Smart compiling to avoid repeased compiling for large projects
- [X] Supports parameters for the Java command

## Versions ##
Developement has been split into two streams, one is a bash script implementation, and the other is written in python.  The bash version is currently functional, but there are still functions I would like to 
implement.  The python version is fully functional, and developement is continuing to move quickly.  I am not currently developing the bash version, and once the python version is more functional, developement on 
the bash front will stop completely.

## Developement ##
Want to get the latest features? Check out the python branch of this project for the most up-to-date version of the tool.  It might not be stable, but you will get the newest features before they hit 
the stable build.

Have an idea for a new feature? Let me know so I can do my best to add it to the tool.
