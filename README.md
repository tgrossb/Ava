## Python ##
This is the version written in python, because bash scripting is honestly the worst.  It is currently ahead of the bash version, and it has potential to go much farther.  This version also 
uses .ini files for configuration, making them far more human readable and easily machine parsable.  Finally, this includes methods for creating and repairing tool and project configuration files, which 
is a big step towards mass use as you don't need to write the skeleton of a configuration file yourself.  Eventually, I want the make project configuration method to create more than just the basic structure 
of a config file by searching the child directories to find libraries, files to be compiled, and the runnable class.

## Dependencies ##
Before downloading and building this tool, some dependencies need to be installed.<br/>
<br/>
This tool requires Python 3.6 or higher.<br/>
You can check which version of Python you have installed with the command:
```bash
python3 --version
```
It should output something like `Python 3.4.2`.<br/>
If you don't have Python 3.6 or higher, follow the intructions in the [Upgrading Python](#upgrading-python) section.<br/>
<br/>
Git makes it much easier to download this repository.  It is not required, as you could download a zip of these files instead, but it is recomended:
```bash
sudo apt-get install git
```

## Building ##
To build this tool, you can use the build script I wrote to create a single runnable. Or, of course, if you're hard core you can build it yourself. Both options 
are here.<br/>
**This is the easy way to build, by using the build tool**:
```bash
git clone https://gitlab.com/tgrossb87/Ava.git
cd Ava
sudo python3 build.py -io
```
If the build script gives you an error saying that the minimum Python version was not met, try running the build script with the Python 3.6 or higher interpreter explicitly.<br/>
This will use the `build` tool to download any Python dependencies, compile all of the Python files into a zipped folder, and export it as a 
runnable to `/usr/local/bin/ava` so the command `ava` can be used from anywhere.<br/>
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
pip install configparser
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
- [ ] Smart compiling to avoid repeated compiling for large projects

## Upgrading Python ##
First, check your Python version.  Assuming you have some minor version of Python 3 already installed, do:
```bash
python3 --version
```
It should output something like `Python 3.4.2`<br/>
Next, download the newest version of Python.  Right now, its Python 3.7:
```bash
sudo apt-get install python3.7
```
This is enough to use Python 3.7, but you will have to type out the full command `python3.7` instead of just `python3` to use this 
interpreter.  If you are okay with this, you don't have to continue on to reasign the symbolic link, but I would recomend continuing.<br/>
The file at `/usr/bin/python3` is a symbolic link to the latest version of Python, so we need to reassign this link:
```bash
sudo ln -sfn /usr/bin/python3.7 /usr/bin/python3
```
Now, Python 3.7 will be the interpreter used when the command `python3` is run.  We can check the version again to be sure:
```bash
python3 --version
```


Have an idea for a new feature? Let me know so I can do my best to add it to the tool.
