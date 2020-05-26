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
* `python3 -m cookiecutter git@dev.rozum.com:rozum-soft/utils/pulse-program-template.git`
  will result in several prompts to be filled (see [params](#cookiecutter-params))
  (change the link when published)
* `cd {{cookiecutter.project_name}}` (*project_name* is filled during template initialization)
* `python3 -m venv venv` will create virtual environment for the project
* `source venv/bin/activate` will activate virtual environment
* `pip install -e . -i https://pip.rozum.com/simple -r requirements/development.txt`
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
is created

* **project_name** - folder containing project and development environment
  * **project_name** - folder containing source code
    * `__init__.py` - identificates that the folder is python package
    * `main.py` - should be used to run program locally during development
    * `program.py` - is used in `main.py` and when the program is executed on 
      the robot side
  * **requirements** - folder containing development/production requirements
    * `development.txt` - is used for development requirements
    * `production.txt` - is used for production requirements
      This file would be used on the robot side to install the dependencies
      needed for the program to be executed properly
  * `MANIFEST.in` - file that contains rules about what files should be included
    into built package
  * `README.md` - is used to place any ne explanatory information about the
    project
  * `setup.py` - is used to build distribution package from source files
  * `upload.py` - is used to build and upload distribution to the robot

**Tip:** you should place your modules/packages in the **package_name/package_name**
folder (near the `__init__.py`).

After the setup the project is ready to be uploaded to the controlbox,
you can do using the command:

`python3 upload.py remote.robot.ip.address`

If you need to upload program to the port that is not the default one (22),
use the following command:

`python3 upload.py remote.robot.ip.address --port your_port_here`

Example, assuming that sandbox is running on `localhost:2222`:

`python3 upload.py localhost --port 2222`
