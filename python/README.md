## Python ##
This is the version written in python, because bash scripting is honestly the worst.  It is currently a little bit behind the bash version, but it has potential to go much farther.  This version also 
uses .ini files for configuration, making them far more human readable and easily machine parsable.  Finally, this includes methods for creating and repairing tool and project configuration files, which 
is a big step towards mass use as you don't need to write the skeleton of a configuration file yourself.  Eventually, I want the make project configuration method to create more than just the basic structure 
of a config file by searching the child directories to find libraries, files to be compiled, and the runnable class.

## Features ##
- [X] Named projects
- [X] Multiple and parallel file compiling
- [X] Automatic running
- [ ] Project and individual logging options
- [X] External library compiling available
- [X] Color and logging per user configurations
- [X] Automatic tool and project configuration file generation
- [ ] Intelligent project configuration generation
- [ ] Clickable error output to take the user to the error (this is a terminal problem, might be a long shot)
- [ ] Normal, verbose, and silent output options
- [ ] Integrated version control (maybe)
- [X] Configuration file look ahead
- [X] Error highlighting in `java` command output

Have an idea for a new feature? Let me know so I can do my best to add it to the tool.
