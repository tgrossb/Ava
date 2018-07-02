# Welcome
Congrats, you have installed Ava.  Welcome to this refrence page with a little bit of a tutorial thrown in.

# Table of contents
&nbsp;1. [The Tool Configuration File](#tool-cfg)  
&nbsp;&nbsp;&nbsp;1.1. [What is it](#tool-cfg-what)  
&nbsp;&nbsp;&nbsp;1.2. [Where is it](#tool-cfg-where)  
&nbsp;&nbsp;&nbsp;1.3. [Parameters](#tool-cfg-params)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.1. [header/footer](#tool-cfg-hf)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.2. [command](#tool-cfg-cmd)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.3. [command output](#tool-cfg-cmd-out)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.4. [warning](#tool-cfg-warn)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.5. [background Warning](#tool-cfg-bwarn)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.6. [error](#tool-cfg-err)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.7. [affirmation](#tool-cfg-affirm)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.8. [line header](#tool-cfg-lineh)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.9. [standard Output](#tool-cfg-stdout)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.10. [log file name](#tool-cfg-log-name)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.11. [logging type](#tool-cfg-log-type)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.3.12. [project configuration file](#tool-cfg-proj-cfg)  
&nbsp;2. [Project Configuration Files](#proj-cfg)  
&nbsp;&nbsp;&nbsp;2.1. [What are they](#proj-cfg-what)  
&nbsp;&nbsp;&nbsp;2.2. [Where are they](#proj-cfg-where)  
&nbsp;&nbsp;&nbsp;2.3. [Parameters](#proj-cfg-params)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.1 [project](#proj-cfg-proj)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.2 [project name](#proj-cfg-proj-name)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.3 [project home](#proj-cfg-proj-home)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.4 [class path](#proj-cfg-class-path)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.5 [compiled destination](#proj-cfg-comp-dest)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.6 [runnable files](#proj-cfg-runnable)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.3.7 [compile files](#proj-cfg-comp-files)  
&nbsp;3. [Commands](#commands)  
&nbsp;&nbsp;&nbsp;3.1 [Make](#cmd-make)  
&nbsp;&nbsp;&nbsp;3.2 [Edit](#cmd-edit)  
&nbsp;&nbsp;&nbsp;3.3 [Verbose](#cmd-verbose)  
&nbsp;&nbsp;&nbsp;3.4 [Quiet](#cmd-quiet)  
&nbsp;&nbsp;&nbsp;3.5 [Silent](#cmd-silent)  
&nbsp;&nbsp;&nbsp;3.6 [Repair tool](#cmd-repair-tool)  
&nbsp;&nbsp;&nbsp;3.7 [Update](#cmd-update)  
&nbsp;4. [Bash Colors](#bash-colors)
&nbsp;5. [Ini Files](#ini-files)  

# <a name="tool-cfg"></a>The Tool Configuration File

## <a name="tool-cfg-what"></a>What is it
The tool configuration file is an [ini file](#ini-files) that defines the style and general configuration of the tool.  This file is populated with default values for [output colors](#bash-colors), 
logging options, and general parameters about [project configuration files](#project-configuration-files).  By default, it looks like [this](.ava.ini).<br/><br/>
Parameters in the tool configuration file mostly control the style of the output of commands.  If you don't like the color of a set of outputs, you can easily redefine it in this file. Color sections have 
comments within them to tell you when they are used, but all of the parameters are defined fully [below](#tool-cfg-params).

## <a name="tool-cfg-where"></a>Where is it
The tool configuration file is in the user's home directory (`~`), and it is a file called `.ava.ini`.  Moving this file will raise a warning, and all default values will be used.  If this happens, you 
can create a new file at `~/.ava.ini` with the [repair tool](#cmd-repair-tool) flag.
<br/><br/>
If you want to know more about each parameter, see the entries [below](#parameters).  If not, continue on to the [next section](#project-configuration-files).

## <a name="tool-cfg-params"></a>Parameters
These are the sections defined in the tool configuration file.  Each section has an explination of when its use and a summary of its associated variables.

#### <a name="tool-cfg-hf"></a>header/footer <span sytle="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to the opening and closing statements of tools in the Ava command set.
<br/><br/>

#### <a name="tool-cfg-cmd"></a>command <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to output that informs the user of commands that are executed internally, like the `javac` and `java` commands.
<br/><br/>

#### <a name="tool-cfg-cmd-out"></a>command output <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to normal output of commands, such as output created by the `java` command.
<br/><br/>

#### <a name="tool-cfg-warn"></a>warning <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to important warnings that are generated.  These warnings can often be resolved easily, but cannot be reliably solved automatically, or require user confirmation.
<br/><br/>

#### <a name="tool-cfg-bwarn"></a>background Warning <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to less important warnings or warnings that supplement full fledged warnings.  For example, missing variables in the tool configuration file generate background warnings, and these 
background warnings culminate in a full warning that includes more general information.
<br/><br/>

#### <a name="tool-cfg-err"></a>error <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to fatal errors generated by compilation, runtime errors generated from the `java` command, and errors created from the tool itself.  For example, if a project configuration file does 
not exist in the parent directories, a fatal error will be raised and highlighted in this color.
<br/><br/>

#### <a name="tool-cfg-affirm"></a>affirmation <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to affirmation statements which ensure that the information recieved by the tool matches what the user intended.  These statements also bring attention to good things.  For example, 
if compilation results in zero errors, it is celebrated with an affirmative statement.
<br/><br/>

#### <a name="tool-cfg-lineh"></a>line header <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is applied to the begining of each line which marks output with the script it's generated by.
<br/><br/>

#### <a name="tool-cfg-stdout"></a>standard Output <span style="font-weight:normal">[`color` ([bash color](#bash-colors)), `bold` (boolean)]</span>
The color defined by `color` and bolded if `bold` evaluates to true is the default color used for output.  All output created by the tool that doesn't fall into some other category uses this color for output.
<br/><br/>

#### <a name="tool-cfg-log-name"></a>log file name <span style="font-weight:normal">[`name` (string)]</span>
The string defined by `name` is the name given to project log files, if the logging type specifies that project logs should be created.
<br/><br/>

#### <a name="tool-cfg-log-type"></a>logging type <span style="font-weight:normal">[`project logging` (boolean), `individual logging` (boolean)]</span>
These variables define which logs are created and kept.<br/>
If `project logging` evaluates to true, a single log file is created in the project home (defined in the project configuration file as [project home](#project-home)).<br/>
If `individual logging` evaluates to true, a log file is created each time the project is compiled and run in the directory where you run from.<br/>
You can set both of these to false to disable logging completely.
<br/><br/>

#### <a name="tool-cfg-proj-cfg-name"></a>project configuration file <span style="font-weight:normal">[`name` (string)]</span>
The string defined by `name` is the name of the [project configuration files](#project-configuration-files) used by the tool.  Project configuration files not with this name will be ignored.

# <a name="proj-cfg"></a>Project Configuration Files

## <a name="proj-cfg-what"></a>What is it
Project configuration files store all of the essential information about the project it is made for.  These files store information about what files should be compiled and run, and where compiled 
files should go to keep everything nice and organized.  This way, you only have to enter your project's information once, not every time you compile and run a project.<br/>
<br/>
Project configuration files can be made by hand, but it is easier to [make](#cmd-make) and [edit](#cmd-edit) them using tool commands.  The default configuration looks like [this](config.ini).<br/>
<br/>
This file has some helpful comments to help you remember what each piece does, but all of the parameters are fully defined [below](#proj-cfg-params).

## <a name="proj-cfg-where"></a>Where is it
Project configuration files are more flexible than [the tool configuration files](#tool-cfg-where).  These files can be anywhere you want, but the first configuration file found in the parent directories 
of where the tool is run is used.  So, if you have a file structure like this:
```
/home/user
  |-- config.ini (for Project A)
  |-- myCode
        |-- config.ini (for Project B)
        |-- ProjectA
        |     |-- src
        |
        |-- ProjectB
              |-- src
```
and you run `ava` from `/home/user/myCode/ProjectA/src`, the configuration file at `/home/user/myCode/config.ini` will be used instead of the configuration file at `/home/user/config.ini`.  For this reason, 
it is recomended that your project configuration files be in the project's home directory.  In other words, the [project home](#proj-cfg-proj-home) variable should simply be `.`.<br/>
So, this file structure should be updated to look like this:
```
/home/user
  |-- myCode
        |-- ProjectA
        |     |-- config.ini (for Project A)
        |     |-- src
        |
        |-- ProjectB
              |-- config.ini (for Project B)
              |-- src
```
**Note: A [warning](#tool-cfg-warn) will be generated if the project configuration file is not in the project's home directory**<br/><br/>
Aside from the location, the file can be named almost anything you want.  See the [project configuration name](#tool-cfg-proj-cfg-name) parameter in the [tool configuration file](#tool-cfg) for more information.

## <a name="proj-cfg-params"></a>Parameters

#### <a name="proj-cfg-proj"></a>project
The `[project]` at the begining is just a requirement of the ini file structure, and its like the root element of an xml document.  You won't need to change this ever, but you need it to be at the top.
<br/><br/>

#### <a name="proj-cfg-proj-name"></a>`project name` (string)
The `project name` variable makes it easier to keep track of your different projects, so we can set this variable to `Tutorial`.  The project name can be as long or short as you want, 
but it cant have any \n charicters.
<br/><br/>


#### <a name="proj-cfg-proj-home"></a>`project home` (path)
The `poject home` variable is very important.  This is the location where log files will be kept if you choose to have them, and it is where project relative paths will be defined from.  This variable is 
represented by the symbol `@` in the rest of the configuration file, and it can be used in paths.  The `@` symbol makes your project highly portable, as it can be redefined when a project moves, and then 
every other path will be recalculated relative to it, even if your configuration file moves as well.
<br/><br/>


#### <a name="proj-cfg-class-path"></a>`class path` (path)
The `class path` variable is where external libraries are defined.  If you have a `lib` folder in your project, you might want to use wildcards (`*`) to include all of the files in that folder in your class 
path.  All external libraries **must** be defined here, and they must be on new lines and indented by either spaces or a tab.
<br/><br/>


#### <a name="proj-cfg-comp-dest"></a>`compiled destination` (path)
The `compiled destination` variable is where files are exported to after they have been compiled.  This is often a bin directory in your project home, which is why it is defined by default as `@/bin`.  And if 
you forget to make the bin folder before you run it, don't worry; Ava can handle the logistics for you.
<br/><br/>

#### <a name="proj-cfg-runnable"></a>`runnable file` (package)
The `runnable file` variable defines the main file which you would normally run.  This is where the Java program begins, and it contains the `static main(String[] args)` function.
<br/><br/>

#### <a name="proj-cfg-comp-files"></a>`compile files` (list<path>)
The `compile files` variable lists all of the `.java` files.  Whenever you create a new file, remember to edit the project configuration file to reflect this change, or it won't be compiled.  Each new file is 
on a new line, and indented by a tab or spaces.

# Commands
## <a name="cmd-make"></a>Make (m)
Makes a [project configuration file](#proj-cfg) populated with [defaults](#config.ini) in the current directory.<br/>
**FUTURE:** Add `[path]` argument to create in any directory.

## <a name="cmd-edit"></a>Edit (e)
Edit into the nearest [project configuration file](#proj-cfg) in the parent directories.<br/>
This will use the default text editor defined in the environment variable $EDITOR, or it defaults to `nano` if one is not defined.<br/>
**FUTURE:** Add `[parameter: value]*` argument to automatically set the value of `parameter` to `value` in that configuration file.

## <a name="cmd-verbose"></a>Verbose (v)
Set the output level to verbose, just print a **bunch** of useless stuff.<br/>
**FUTURE:** What? Nothing.

## <a name="cmd-quiet"></a>Quiet (q)
Suppress some of the output to remove some peace-of-mind output.<br/>
**FUTURE:** I don't know, make other things quite?

## <a name="cmd-silent"></a>Silent (s)
Suppress all output except headers, footers, errors, and `java` output.<br/>
**FUTURE:** What would I even change?

## <a name="cmd-repair-tool"></a>Repair Tool (r)
Repairs the tool configuration file at `~/.ava.ini` by filling in missing sections and parameters with defaults, or maybe creating a whole new file.<br/>
**FUTURE:** I guess it could look for the file if its missings.

## <a name="cmd-update"></a>Update (u)
Yeah, not going to lie, this straight up does not work right now.<br/>
**FUTURE:** Make it work!

# Bash Colors
This is a specific way of defining colors to be printed in x enabled terminal environments.  
Here are some pages you can visit for more information:
- https://misc.flogisoft.com/bash/tip_colors_and_formatting (my favorite)
- https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux (of course I have a stack overflow link)
- http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html (this one's eh)

# Ini Files
Ini files are simple text files used for configuration.  
Here are some pages you can visit for more information:
- https://en.wikipedia.org/wiki/INI_file (has good examples)


Thats all I got.  Its kind of proprietary and I kind of hate it, so I may switch this soon.  Look out for that.
