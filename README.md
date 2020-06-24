# Pulse program template

Template to create Python programs for Pulse Program Player.

## Concept

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for
Pulse Robotic Arm Program Player. The main idea behind this project is to create
easy to use development environment with predefined structure so that it gives
an opportunity to create, test, deploy and run programs for 
[Pulse Robotic Arm](https://rozum.com/robotic-arm/).

## Requirements

Python 3.5+

## Installation

* Python 3.5+ required 
  (on Debian-based linux run `sudo apt-get install python3-dev python3-venv`)
* `python3 -m pip install cookiecutter --user`
* `python3 -m cookiecutter git@gitlab.com:rozumrobotics/rozum-developers/utils/pulse-program-template.git`
  will result in several prompts to be filled (see [params](#cookiecutter-params))
  (change the link when published)
* `cd {{cookiecutter.project_name}}` (*project_name* is filled during template initialization)
* `python3 -m venv venv` will create virtual environment for the project
* `source venv/bin/activate` will activate virtual environment
* `pip install -e . -r requirements/development.txt`
  will install development requirements.

## Cookiecutter params
```json
{
    "project_name": "helloworld", // name of the project folder and the package inside.
    // MUST be a valid python module/package name, see: https://docs.python-guide.org/writing/structure/#modules 
    "email": "dev@rozum.com", // optional email
    "author": "Rozum Robotics", // optional author
    "url": "https://rozum.com", // optional url
    "version": "0.0.1", // initial version of the project
    "pulse_api_version": "1.6.0" //pulse-api version to use in the project
}
```

## Initial project structure

After completing the installation steps, the project of the following structure
is created:

* **project_name** - folder containing project and development environment.
  * **project_name** - folder containing source code.
    * `__init__.py` - identificates that the folder is python package.
    * `main.py` - should be used to run program locally during development.
    * `program.py` - is used in `main.py` and when the program is executed on 
      the robot side. **IMPORTANT:** Do not rename this file.
  * **requirements** - folder containing development/production requirements.
    * `development.txt` - is used for development requirements.
    * `production.txt` - is used for production requirements.
      This file would be used on the robot side to install the dependencies
      needed for the program to be executed properly.
  * `MANIFEST.in` - file that contains rules about what files should be included
    into built package.
  * `README.md` - is used to place any ne explanatory information about the
    project.
  * `setup.py` - is used to build distribution package from source files.
  * `upload.py` - is used to build and upload distribution to the robot.

**Tip:** you should place your modules/packages in the **package_name/package_name**
folder (near the `__init__.py`).

## program.py structure

There is a predefined `Instance` class that is used to store the program logic.
There are predefined methods where you should place your logic.

**IMPORTANT:** You must not rename or remove mentioned methods and class name.
Such actions would result in runtime errors. If you do not need some methods,
put the `pass` keyword inside and leave them blank.

* `__init__` and `__enter__` - used for the program instance initialization.
  **Should not be modified.**
* `__exit__` - used for program instance deinitialization. Invokes the
  `on_error()` method passing the exception value if it is present.
* `before_all()` - will be executed once before the the other methods.
  It is a good place to put initialization logic. For example, set the starting
  pose/position for the robot or enable necessary devices
* `before_each()` - will be executed before each iteration. It is a good place
  to put starting logic. For example, ask the robot to go to the first point in 
  iteration and/or enable the tooling installed.
* `execute()` - represents one iteration. Place any logic that is needed to be
  done during iteration here.
* `after_each()` - will be executed after each iteration. It is a good place to
  put iteration finalization logic. For example, ask the robot to go to the last
  point in iteration and/or disable the tooling installed.
* `after_all()` - will be executed once after the user stops the program.
  It is a good place to put complete finalization logic. For example, ask the
  robot to switch off the devices and go to the final position.
* `on_error()` - will be executed on any runtime error that is not caught by
  the user code. It is a good place for logic that would provide safe
  deitialization of the robot and devices.

## Execution and deployment

### Local execution

To run the program locally, after the template is filled with necessary logic,
use the following command (remember to activate the virtual environment):

`python3 -m project_name.main -i number_of_iterations --robot-addr robot_addr_goes_here`

For example you want the robot that is located at the known network address
(e.g. 192.168.0.24) perform two iterations using code from your project
(named `some_program`, for example purposes).
Use the following command to achieve this behavior:

`python3 -m some_program.main -i 2 --robot-addr http://192.168.0.24:8081`

This should result in the following execution sequence:
* before_all
* Repeat 2 times:
  * before_each
  * execute
  * after_each
* after_all
* If there are any runtime errors during the execution on_error is called 

## Program deployment

Lets assume that robot is located at the known network address
(e.g. 192.168.0.24). You tested the program locally and you want to deploy
program on robot for future usage. You can do this using the following command
(remember to activate the virtual environment):

`python3 upload.py 192.168.0.24`

If you need to upload program to the port that is not the default one
(e.g. 2222, instead of the default one - 22), use the following command:

`python3 upload.py 192.168.0.24 --port 2222`

If there are any errors during upload, you can enable verbose logging,
by passing the `--verbose` parameter to the command:

`python3 upload.py 192.168.0.24 --verbose`

If you still can not deal with the error - contact the developers/support and
attach the `upload.log` file which can be generated by passing the `--dump-log`
parameter to the command. Also, please, write the actions that took part before.
Example command to dump detailed log:

`python3 upload.py 192.168.0.24 --verbose --dump-log`
