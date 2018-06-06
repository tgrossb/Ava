## Python ##
This is the version written in python, because bash scripting is honestly the worst.  It is currently a little bit behind the bash version, but it has potential to go much farther.  This version also 
uses .ini files for configuration, making them far more human readable and easily machine parsable.  Finally, this includes methods for creating and repairing tool and project configuration files, which 
is a big step towards mass use as you don't need to write the skeleton of a configuration file yourself.  Eventually, I want the make project configuration method to create more than just the basic structure 
of a config file by searching the child directories to find libraries, files to be compiled, and the runnable class.

## Creating a single runnable ##
I am working on making the releaser tool in the release directory for easy generation.  Currently though, these commands can be used reliably to make a single runnable.
```
cd release
mkdir avaRelease
cp ../*.py __main__.py avaRelease
cd avaRelease && zip -r ../inter.zip * && cd ..
echo '#!/usr/bin/env python3' | cat - inter.zip > ava
chmod +x ava
rm inter.zip
```
This will create a runnable file called `ava` that you can then move to your `/usr/local/bin/` file or move it to where you would like and add it to your `PATH` variable. The `releaser` script 
is something I'm working on that does this, but it is fairly untested, so use at your own risk.

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
