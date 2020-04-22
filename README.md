# Pulse program template

Template to create Python programs for Pulse Program Player.

## Configuration
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

## Usage

Install cookiecutter:

`python3 -m pip install cookiecutter --user`

Go to directory where you want to start your project and initiate it:

```bash
cd workdir
python3 -m cookiecutter git@dev.rozum.com:rozum-soft/utils/pulse-program-template.git
```

Fill in the fields and start developing at project_name/project_name folder.

**Note:** It is recommended to create and activate python virtual environment
prior to execution of any other commands.
You can do this with following commands:

```bash
cd project_name
python3 -m venv venv
source venv/bin/activate
```

To test that project initiated properly and install development requirements, run:

`pip install -e . -i https://pip.rozum.com/simple -r requirements/development.txt`

After the setup the project is ready to be uploaded to the controlbox,
you can do using the command:

`python3 upload.py remote.robot.ip.address`

If you need to upload program to the port that is not the default one (22),
use the following command:

`python3 upload.py remote.robot.ip.address --port your_port_here`

Example, assuming that sandbox is running on `localhost:2222`:

`python3 upload.py localhost --port 2222`
