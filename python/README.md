## Python ##
This is the version written in python, because bash scripting is honestly the worst.  It is currently a little bit behind the bash version, but it has potential to go much farther.  This version also 
uses .ini files for configuration, making them far more human readable and easily machine parsable.  Finally, this includes methods for creating and repairing tool and project configuration files, which 
is a big step towards mass use as you don't need to write the skeleton of a configuration file yourself.  Eventually, I want the make project configuration method to create more than just the basic structure 
of a config file by searching the child directories to find libraries, files to be compiled, and the runnable class.

## Building ##
To build this tool, you can use the simple bash script I wrote to create a single runnable. Or, of course, if you're hard core you can build it yourself. Both options 
are here.<br/>
**This is the easy way to build, by using the build tool**:
```bash
cd ava/python
sudo ./build -i -o ava
```
This will use the `build` tool to compile all of the python files into a zipped folder and export it as a runnable to `/usr/local/bin/ava` so the command `ava` can be used from anywhere.<br/>
Or, if you really want, you could build it yourself:
```bash
cd ava/python
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
to your `PATH` variable. I would recommend using the tool though, its much easier.

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

Have an idea for a new feature? Let me know so I can do my best to add it to the tool.
